import psutil
import re
import os
import signal
import datetime
import uuid
import logging
import glob
import subprocess


class NoHostException(Exception):
    pass


class Rsync:
    """
    This gives an overall percentage progress through the file transfer
    rsync --info=progress2 OfficeTable:/media/share/Software/ISO/Linux/*.* . > /tmp/t.log
    For pause/resume include the --partial option
    rsync --info=progress2 --partial OfficeTable:/media/share/Software/ISO/Linux/*.* . > /tmp/t.log
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

        logging.debug([
            'rsync',
            '--info=progress2',
            '--partial',
            '--recursive',
            source,
            dest
        ])
        # TODO: Should use the tempfile library here as this does not work in CentOS for some reason.
        with open('/tmp/rsync_%s.log' % uuid.uuid4(), 'w') as logfile:
            psutil.Popen(
                [
                    'rsync',
                    '--info=progress2',
                    '--partial',
                    '--recursive',
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
        for file in glob.iglob('/tmp/rsync_*.log'):
            if file not in current_logs:
                os.remove(file)

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
        :param log_file:
        :return:
        """
        if log_file is None or not os.path.isfile(log_file):
            return -1

        logging.debug('Fetching rsync progress from {}'.format(log_file))
        log = open(log_file, 'r')
        content = log.read()
        log.close()
        matches = re.findall(' (\d*)\% ', content)
        if len(matches) > 0:
            logging.debug('Progress {}%'.format(matches[-1]))
            return matches[-1]

        logging.debug('Could not acquire progress')
        return 100

    def find_log_file(self, open_files):
        for open_file in open_files:
            if open_file[0][:11] == "/tmp/rsync_" and open_file[0][-4:] == ".log":
                return open_file[0]

        return None
