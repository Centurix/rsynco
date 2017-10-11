import cherrypy
from rsynco.libs.repositories.host_repository import HostRepository
from .apihandler import ApiHandler
from rsynco.libs.validation import validation
from rsynco.api.transformers.host_transformer import HostTransformer


class Hosts(ApiHandler):
    def __init__(self):
        self._hostRepository = HostRepository()

    def GET(self, name=None):
        if name is not None:
            return HostTransformer.hosts([self._hostRepository.get_host(name)])

        return HostTransformer.hosts(self._hostRepository.get_all_hosts())

    @validation
    def POST(self):
        data = cherrypy.request.json['data'][0]['attributes']
        self._hostRepository.add_host(
            data['host'],
            data['hostname'],
            data['port'],
            data['username'],
            data['password']
        )
        cherrypy.response.status = 201
        return HostTransformer.hosts([data])

    @validation
    def PUT(self, name):
        data = cherrypy.request.json['data'][0]['attributes']
        self._hostRepository.update_host(
            name,
            data['hostname'],
            data['port'],
            data['username'],
            data['password']
        )
        return HostTransformer.hosts([data])

    def DELETE(self, name):
        self._hostRepository.delete_host(name)
        return {'data': 'DELETED'}
