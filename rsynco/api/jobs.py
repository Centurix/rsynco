import cherrypy
from .apihandler import ApiHandler
from rsynco.libs.storage import Storage


class Jobs(ApiHandler):
    def __init__(self):
        self._storage = Storage()

    def GET(self, name=None):
        if name is not None:
            return {'data': self._storage.get_job(name)}

        return {'data': self._storage.get_jobs()}

    def POST(self):
        data = cherrypy.request.json
        self._storage.add_job(
            data['name'],
            data['from_host'],
            data['from_path'],
            data['to_host'],
            data['to_path']
        )
        return {'data': 'ADDED'}

    def PUT(self, name):
        data = cherrypy.request.json
        self._storage.update_job(
            name,
            data['from_host'],
            data['from_path'],
            data['to_host'],
            data['to_path']
        )
        return {'data': 'UPDATED'}

    def DELETE(self, name):
        self._storage.delete_job(name)
        return {'data': 'DELETED'}
