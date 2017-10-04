import psutil
import re
import os
import signal


class Rsync:
    """
    This gives an overall percentage progress through the file transfer
    rsync --info=progress2 OfficeTable:/media/share/Software/ISO/Linux/*.* . > /tmp/t.log
    For pause/resume include the --partial option
    rsync --info=progress2 --partial OfficeTable:/media/share/Software/ISO/Linux/*.* . > /tmp/t.log
    """
    def __init__(self):
        pass

    def list_rsync_tasks(self):
        tasks = list()
        for proc in psutil.process_iter():
            if proc.name() == 'rsync' and len(proc.children()) == 0:
                tasks.append({
                    'pid': proc.pid,
                    'started': proc._create_time,
                    'from': self.get_from(),
                    'to': self.get_to(),
                    'progress': self.get_progress(proc.pid),
                    'status': proc.status()
                })
        return tasks

    def pause(self, pid):
        os.kill(pid, signal.SIGTSTP)

    def resume(self, pid):
        os.kill(pid, signal.SIGCONT)

    def stop(self, pid):
        os.kill(pid, signal.SIGTERM)

    def get_progress(self, pid):
        """
        Check /tmp/pid for the process output to check for output and scan for progress
        If the log file doesn't exist then the process isn't being monitored by synco
        :param pid:
        :return:
        """
        if os.path.isfile('/tmp/t.log'):
            log = open('/tmp/t.log', 'r')
            content = log.read()
            log.close()
            matches = re.findall(' (\d*)\% ', content)
            if len(matches) > 0:
                return matches[-1]

        return 0

    def get_from(self):
        return "/home/chris"

    def get_to(self):
        return "/media"
