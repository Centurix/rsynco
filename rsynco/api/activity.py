from rsynco.libs.rsync import Rsync
from .apihandler import ApiHandler
import logging


class Activity(ApiHandler):
    def GET(self):
        logging.debug('API: Getting rsync activity')
        test = Rsync()
        return {'data': test.list_rsync_tasks()}

    def POST(self, pid, action):
        test = Rsync()
        if action == "pause":
            logging.debug('API: Pausing {}'.format(pid))
            test.pause(int(pid))
            return {'data': 'PAUSED'}
        elif action == "resume":
            logging.debug('API: Resuming {}'.format(pid))
            test.resume(int(pid))
            return {'data': 'RESUMED'}
        elif action == "stop":
            logging.debug('API: Stopping {}'.format(pid))
            test.stop(int(pid))
            return {'data': 'STOPPED'}

        logging.debug('API: Invalid operation')
        return {'data': 'NO_ACTION'}
