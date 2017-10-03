import sys
import os
import time
import atexit
import signal


class Daemon:
    EXIT_OK = 0
    EXIT_OTHER_ERROR = 1
    EXIT_PARAM_ERROR = 2

    def __init__(self, pidfile):
        self.pidfile = pidfile

    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(self.EXIT_OK)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(self.EXIT_OTHER_ERROR)

        os.chdir('/')
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(self.EXIT_OK)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(self.EXIT_OTHER_ERROR)

        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        try:
            with open(self.pidfile, 'r') as pf:

                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pidfile {0} already exist. Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(self.EXIT_OTHER_ERROR)

        self.daemonize()
        self.run()

    def stop(self):
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pidfile {0} does not exist. Daemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            return

        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(self.EXIT_OTHER_ERROR)

    def restart(self):
        self.stop()
        self.start()

    def status(self):
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "Service not running\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(self.EXIT_OTHER_ERROR)

        try:
            os.kill(pid, 0)
        except OSError as err:
            message = "Service not running\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(self.EXIT_OTHER_ERROR)

        message = "Service running\n"
        sys.stderr.write(message.format(self.pidfile))
        sys.exit(self.EXIT_OTHER_ERROR)


    def run(self):
        pass
