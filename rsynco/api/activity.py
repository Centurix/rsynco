from rsynco.libs.rsync import Rsync
from .apihandler import ApiHandler
import logging
from rsynco.api.transformers.activity_transformer import ActivityTransformer
import cherrypy
from rsynco.libs.validation import validation


class Activity(ApiHandler):
    def __init__(self):
        self._rsync = Rsync()

    def GET(self):
        """
        Endpoint: /activity
        Return: 200 OK

        :return:
        """
        logging.debug('API: Getting rsync activity')
        return ActivityTransformer.activities(self._rsync.list_rsync_tasks())

    @validation
    def PATCH(self, pid):
        """
        Perform actions based on the state field
        """
        data = cherrypy.request.json['data'][0]['attributes']
        if data['status'] == 'pause':
            logging.debug('API: Pausing {}'.format(pid))
            self._rsync.pause(int(pid))
        elif data['status'] == 'resume':
            logging.debug('API: Resuming {}'.format(pid))
            self._rsync.resume(int(pid))
        elif data['status'] == 'stop':
            logging.debug('API: Stopping {}'.format(pid))
            self._rsync.stop(int(pid))
        else:
            logging.debug('API: No action {}'.format(pid))

        return ActivityTransformer.activities([self._rsync.get_rsync_task(int(pid))])
