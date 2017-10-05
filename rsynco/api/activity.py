import cherrypy
from rsynco.libs.rsync import Rsync
from rsynco.libs.storage import Storage


class Activity(object):
    exposed = True

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.tools.json_out(content_type='application/vnd.api+json')
    def GET(self):
        test = Rsync()
        return {'data': test.list_rsync_tasks()}

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.tools.json_out(content_type='application/vnd.api+json')
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

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.tools.json_out(content_type='application/vnd.api+json')
    def PUT(self):
        test = Rsync()
        test.process('OfficeTable:/media/share/Software/ISO/Linux/*.*', '/home/chris/Desktop/iso')
        return {'data': 'STARTED'}

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.tools.json_out(content_type='application/vnd.api+json')
    def OPTIONS(self):
        return {'data': 'OK'}

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.tools.json_out(content_type='application/vnd.api+json')
    def DELETE(self):
        storage = Storage()
        return storage.get_hosts()
