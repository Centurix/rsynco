from rsynco.libs.rsync import Rsync
from rsynco.libs.storage import Storage
from .apihandler import ApiHandler


class Activity(ApiHandler):
    def __init__(self):
        self._storage = Storage()

    def GET(self):
        test = Rsync()
        return {'data': test.list_rsync_tasks()}

    def POST(self, pid, action):
        test = Rsync()
        if action == "pause":
            test.pause(int(pid))
            return {'data': 'PAUSED'}
        elif action == "resume":
            test.resume(int(pid))
            return {'data': 'RESUMED'}
        elif action == "stop":
            test.stop(int(pid))
            return {'data': 'STOPPED'}

        return {'data': 'NO_ACTION'}
