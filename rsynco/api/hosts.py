import cherrypy
from rsynco.libs.storage import Storage


@cherrypy.tools.accept(media='application/json')
@cherrypy.tools.json_out(content_type='application/vnd.api+json')
@cherrypy.tools.json_in()
@cherrypy.expose
class Hosts(object):
    def __init__(self):
        self._storage = Storage()

    def GET(self, name=None):
        if name is not None:
            return {'data': self._storage.get_host(name)}

        return {'data': self._storage.get_hosts()}

    def POST(self):
        data = cherrypy.request.json
        self._storage.add_host(
            data['host'],
            data['hostname'],
            data['port'],
            data['username'],
            data['password']
        )
        return {'data': 'ADDED'}

    def PUT(self, name):
        data = cherrypy.request.json
        lines = self._storage.update_host(
            name,
            data['hostname'],
            data['port'],
            data['username'],
            data['password']
        )
        return {'data': lines}

    def OPTIONS(self, *args):
        return {'data': 'OK'}

    def DELETE(self, name):
        self._storage.delete_host(name)
        return {'data': 'DELETED'}
