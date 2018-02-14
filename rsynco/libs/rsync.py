import psutil
import re
import os
import signal
import datetime
import logging
import glob
import subprocess
import tempfile


class NoHostException(Exception):
    pass


class Rsync:
    """
    For rsync 3.1+
    ==============

    This gives an overall percentage progress through the file transfer
    rsync --info=progress2 Server:/media/share/Software/ISO/Linux/*.* . > /tmp/t.log
    For pause/resume include the --partial option
    rsync --info=progress2 --partial Server:/media/share/Software/ISO/Linux/*.* . > /tmp/t.log

    This is nice, but there are quite a few distros where rsync isn't this up to date

    For rsync prior to 3.1
    ======================

    Ref: https://lists.samba.org/archive/rsync/2011-October/027025.html

    We handle pre 3.1.0 rsync by doing a dry run, parsing the output for the count of files

    rsync -r [src] [dst] --dry-run --out-format=""

    This outputs a quick test giving the list of files, types, sizes and total transfer size,
    we then use this when we do the real transfer to work out where we are.

    %f = Filename
    %i = >f+++++++++ (file, plus direction <>) cd+++++++++ (dir)
    %l = File byte size

    rsync -r user@server:/home/user/transfer/ . --dry-run --out-format="['%i','%f','%l']"

    We annotate the header of the log file for each transfer with the details we need:

    --------------------------------------------
    ['>f+++++++++','.keep','24']
    ['>f+++++++++','video.mkv','210085346']
    ['>f+++++++++','video2.mkv','210085346']
    ['cd+++++++++','test','4096']
    ['>f+++++++++','test/video3.avi','442853376']
    ...Rest of the log
    --------------------------------------------
    """
    def __init__(self):
        pass

    def process(self, from_host, from_path, to_host, to_path):
        if from_host is None or to_host is None:
            raise NoHostException('Invalid host configuration, rsync not started')

        if from_host['type'] == 'system':
            source = '{}:{}'.format(from_host['host'], from_path)
            dest = '{}:{}'.format(to_host['host'], to_path)
        else:
            source = '{}:{}'.format(from_host['hostname'], from_path)
            dest = '{}:{}'.format(to_host['hostname'], to_path)

        if from_host['hostname'] == 'localhost':
            source = from_path

        if to_host['hostname'] == 'localhost':
            dest = to_path

        if source[-1] != '/':
            source = source + '/'

        if dest[-1] != '/':
            dest = dest + '/'

        with tempfile.NamedTemporaryFile(mode='w+', prefix='rsync_') as logfile:
            logging.info('DUMPING TO LOG FILE: {}'.format(logfile.name))
            psutil.Popen(
                [
                    'rsync',
                    '--dry-run',
                    '--recursive',
                    '--out-format=[%i,%f,%l]',
                    source + '/',
                    dest
                ],
                stdout=logfile
            )
            os.wait()
            psutil.Popen(
                [
                    'rsync',
                    '--recursive',
                    '--progress',
                    source + '/',
                    dest
                ],
                stdout=logfile
            )
            os.wait()
        return

    def get_rsync_task(self, pid):
        try:
            proc = psutil.Process(pid)
            return {
                'pid': proc.pid,
                'started': datetime.datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
                'from': proc.cmdline()[-2],
                'to': proc.cmdline()[-1],
                'progress': self.get_progress(self.find_log_file(proc.open_files())),
                'status': proc.status(),
                'type': self.task_type(proc)
            }
        except psutil.NoSuchProcess as ex:
            logging.debug('No such process {}'.format(pid))
            return {'pid': '', 'started': 0, 'from': '', 'to': '', 'progress': 0, 'status': 'stopped'}

    def list_rsync_tasks(self):
        logging.debug('Acquiring a list of current rsync tasks...')
        tasks = list()
        active_log_files = list()
        for proc in psutil.process_iter():
            try:
                if proc.name() == 'rsync' and len(proc.children()) == 0:
                    active_log_files.append(self.find_log_file(proc.open_files()))
                    tasks.append({
                        'pid': proc.pid,
                        'started': datetime.datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
                        'from': proc.cmdline()[-2],
                        'to': proc.cmdline()[-1],
                        'progress': self.get_progress(self.find_log_file(proc.open_files())),
                        'status': proc.status(),
                        'type': self.task_type(proc)
                    })
            except psutil.NoSuchProcess:
                pass  # Probably caught the process terminating before probing for its details, that's ok

        logging.debug('Active log files:')
        logging.debug(active_log_files)

        self.cull_dead_logs(active_log_files)

        return tasks

    def task_type(self, proc):
        if "--server" in proc.cmdline():
            return "server"

        return "client"

    def cull_dead_logs(self, current_logs):
        for file in glob.iglob(os.path.join(tempfile.gettempdir(), 'rsync_*')):
            if file not in current_logs:
                try:
                    os.remove(file)
                except PermissionError as pe:
                    logging.debug('Unable to clear log file {}'.format(file))

    def pause(self, pid):
        logging.debug('Pausing rsync task {}...'.format(pid))
        os.kill(pid, signal.SIGSTOP)

    def resume(self, pid):
        logging.debug('Resuming rsync task {}...'.format(pid))
        os.kill(pid, signal.SIGCONT)

    def stop(self, pid):
        logging.debug('Stopping rsync task {}...'.format(pid))
        os.kill(pid, signal.SIGTERM)

    def exists(self):
        logging.debug('Checking for existence of rsync...')
        try:
            process = psutil.Popen(['rsync', '--version'], stdout=subprocess.PIPE)
            stdout, stderr = process.communicate(input=None)
        except FileNotFoundError as fnf:
            return False

        return True

    def version(self):
        logging.debug('Getting rsync version...')

        process = psutil.Popen(['rsync', '--version'], stdout=subprocess.PIPE)
        stdout, stderr = process.communicate(input=None)

        matches = re.findall(b'version (\d*)\.(\d*)\.(\d*) ', stdout)
        if len(matches) == 0:
            return 0

        if len(matches[0]) != 3:
            return 0

        return float('{}.{}'.format(int(matches[0][0]), int(matches[0][1])))

    def get_progress(self, log_file):
        """
        Check /tmp/pid for the process output to check for output and scan for progress
        If the log file doesn't exist then the process isn't being monitored by rsynco
        Calculate the total percentage through the transfer from the log.
        :param log_file:
        :return:
        """
        if log_file is None or not os.path.isfile(log_file):
            return -1

        logging.debug('Fetching rsync progress from {}'.format(log_file))
        log = open(log_file, 'r')
        content = log.read()
        log.close()

        # Get the total count of files and the total file sizes
        all_files = re.findall('\[>f\+*,(.*),(\d*)\]', content)
        processed_files = re.findall('(.*)\n\n.*0\%', content)
        current_percent = int(re.findall('(\d*)\%', content)[-1])
        current_file = processed_files[-1]

        file_total = 0
        for file in all_files:
            file_total = file_total + int(file[1])

        progress_total = 0
        for processed_file in processed_files:
            for file in all_files:
                if processed_file == file[0]:
                    if processed_file != current_file:
                        progress_total = progress_total + int(file[1])
                    else:
                        progress_total = progress_total + int(int(file[1]) / 100 * current_percent)

        return int(float(progress_total) / file_total * 100)

    def find_log_file(self, open_files):
        for open_file in open_files:
            if open_file[0].startswith(os.path.join(tempfile.gettempdir(), 'rsync_')):
                return open_file[0]

        return None
