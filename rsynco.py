#!/usr/bin/env python3
import sys
from rsynco.rsynco_daemon import RsyncoDaemon
from configobj import ConfigObj
from validate import Validator


EXIT_OK = 0
EXIT_OTHER_ERROR = 1
EXIT_PARAM_ERROR = 2

config_file = 'rsynco.ini'
config_spec = 'configspec.ini'

if __name__ == "__main__":
    config = ConfigObj(config_file, configspec=config_spec)
    validator = Validator()

    if not config.validate(validator):
        print("Invalid configuration file")
        sys.exit(EXIT_PARAM_ERROR)

    daemon = RsyncoDaemon(config['pidfile'])
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
