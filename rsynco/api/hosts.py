import cherrypy
from rsynco.libs.repositories.host_repository import HostRepository
from .apihandler import ApiHandler
from rsynco.libs.validation import validation


class Hosts(ApiHandler):
    def __init__(self):
        self._hostRepository = HostRepository()

    def GET(self, name=None):
        if name is not None:
            return {'data': self._hostRepository.get_host(name)}

        return {'data': self._hostRepository.get_all_hosts()}

    @validation
    def POST(self):
        data = cherrypy.request.json['data']['attributes']
        self._hostRepository.add_host(
            data['host'],
            data['hostname'],
            data['port'],
            data['username'],
            data['password']
        )
        return {'data': 'ADDED'}

    @validation
    def PUT(self, name):
        data = cherrypy.request.json['data']['attributes']
        self._hostRepository.update_host(
            name,
            data['hostname'],
            data['port'],
            data['username'],
            data['password']
        )
        return {'data': 'UPDATED'}

    def DELETE(self, name):
        self._hostRepository.delete_host(name)
        return {'data': 'DELETED'}
