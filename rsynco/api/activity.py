import cherrypy
from rsynco.libs.rsync import Rsync
from rsynco.libs.storage import Storage


@cherrypy.tools.accept(media='application/json')
@cherrypy.tools.json_out(content_type='application/vnd.api+json')
@cherrypy.tools.json_in()
@cherrypy.expose
class Activity(object):
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

        return {'data': 'NO_ACTION'}

    def OPTIONS(self):
        return {'data': 'OK'}
