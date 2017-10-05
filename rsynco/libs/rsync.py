import psutil
import re
import os
import signal
import datetime
import uuid


class Rsync:
    """
    This gives an overall percentage progress through the file transfer
    rsync --info=progress2 OfficeTable:/media/share/Software/ISO/Linux/*.* . > /tmp/t.log
    For pause/resume include the --partial option
    rsync --info=progress2 --partial OfficeTable:/media/share/Software/ISO/Linux/*.* . > /tmp/t.log
    """
    def __init__(self):
        pass

    def process(self, from_location, to_location):
        with open('/tmp/rsync_%s.log' % uuid.uuid4(), 'w') as logfile:
            psutil.Popen(
                ['rsync', '--info=progress2', '--partial', from_location, to_location],
                stdout=logfile
            )
            os.wait()
        return

    def list_rsync_tasks(self):
        tasks = list()
        for proc in psutil.process_iter():
            if proc.name() == 'rsync' and len(proc.children()) == 0:
                tasks.append({
                    'pid': proc.pid,
                    'started': datetime.datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
                    'from': proc.cmdline()[-2],
                    'to': proc.cmdline()[-1],
                    'progress': self.get_progress(self.find_log_file(proc.open_files())),
                    'status': proc.status()
                })
        return tasks

    def pause(self, pid):
        os.kill(pid, signal.SIGTSTP)

    def resume(self, pid):
        os.kill(pid, signal.SIGCONT)

    def stop(self, pid):
        os.kill(pid, signal.SIGTERM)

    def get_progress(self, log_file):
        """
        Check /tmp/pid for the process output to check for output and scan for progress
        If the log file doesn't exist then the process isn't being monitored by rsynco
        :param log_file:
        :return:
        """
        if log_file is None or not os.path.isfile(log_file):
            return -1

        log = open(log_file, 'r')
        content = log.read()
        log.close()
        matches = re.findall(' (\d*)\% ', content)
        if len(matches) > 0:
            return matches[-1]

        return 100

    def find_log_file(self, open_files):
        for open_file in open_files:
            if open_file[0][:11] == "/tmp/rsync_" and open_file[0][-4:] == ".log":
                return open_file[0]

        return None
