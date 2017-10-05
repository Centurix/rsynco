#!/usr/bin/env python3
import sys
import os
from rsynco import Config
from rsynco.rsynco_daemon import RsyncoDaemon

EXIT_OK = 0
EXIT_OTHER_ERROR = 1
EXIT_PARAM_ERROR = 2

config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rsynco.ini')
config_spec = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configspec.ini')


if __name__ == "__main__":
    config = Config(config_file, config_spec)

    if config.data is None:
        print("Invalid configuration file")
        sys.exit(EXIT_PARAM_ERROR)

    daemon = RsyncoDaemon(config.data['pidfile'])
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print("Unknown command")
            sys.exit(EXIT_PARAM_ERROR)
        sys.exit(EXIT_OK)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(EXIT_PARAM_ERROR)
