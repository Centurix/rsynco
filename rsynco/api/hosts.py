import cherrypy
from rsynco.libs.storage import Storage
from .apihandler import ApiHandler


class Hosts(ApiHandler):
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
        self._storage.update_host(
            name,
            data['hostname'],
            data['port'],
            data['username'],
            data['password']
        )
        return {'data': 'UPDATED'}

    def DELETE(self, name):
        self._storage.delete_host(name)
        return {'data': 'DELETED'}
