#!/usr/bin/env python3
import sys
import os
from rsynco import Config
from rsynco.rsynco_daemon import RsyncoDaemon
import logging
from rsynco.libs.rsync import Rsync


EXIT_OK = 0
EXIT_OTHER_ERROR = 1
EXIT_PARAM_ERROR = 2

config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rsynco.ini')
config_spec = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configspec.ini')


def usage():
    logging.info("usage: %s start|stop|restart" % sys.argv[0])


if __name__ == "__main__":
    config = Config(config_file, config_spec)

    if config.data is None:
        print("Invalid configuration file")
        sys.exit(EXIT_PARAM_ERROR)

    logging.basicConfig(
        filename=config.data['log_file'],
        level=logging.DEBUG
    )
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    daemon = RsyncoDaemon(config.data['pidfile'])
    rsync = Rsync()
    if not rsync.exists():
        logging.error('RSYNC NOT INSTALLED, EXITING...')
        sys.exit(EXIT_OTHER_ERROR)

    version = rsync.version()

    logging.info('Found rsync version {}'.format(version))
    if version < 3.1:
        logging.warning('RSYNC VERSION IS BELOW 3.1, SOME FUNCTIONALITY WILL BE UNAVAILABLE')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            logging.info('Starting rsynco...')
            daemon.start()
        elif 'stop' == sys.argv[1]:
            logging.info('Stopping rsynco...')
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            logging.info('Re-starting rsynco...')
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            logging.warning('Unknown command "%s"' % sys.argv[1])
            usage()
            sys.exit(EXIT_PARAM_ERROR)
        sys.exit(EXIT_OK)
    else:
        usage()
        sys.exit(EXIT_PARAM_ERROR)
