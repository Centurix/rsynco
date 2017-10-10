import cherrypy
from rsynco.libs.repositories.host_repository import HostRepository
from .apihandler import ApiHandler
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json


class Hosts(ApiHandler):
    def __init__(self):
        self._hostRepository = HostRepository()

    def GET(self, name=None):
        if name is not None:
            return {'data': self._hostRepository.get_host(name)}

        return {'data': self._hostRepository.get_all_hosts()}

    def POST(self):
        # Validate the incoming json
        # TODO: Move this schema validation to the ApiHandler and resolve invisibly
        try:
            # Grab the schema
            with open('/home/chris/Projects/PycharmProjects/rsynco/rsynco/api/schema/hosts/post.json', 'r') as schema:
                schema_contents = schema.read()

            validate(cherrypy.request.json, json.loads(schema_contents))
        except ValidationError as validation_error:
            cherrypy.response.status = 400
            return {'data': validation_error.message}

        data = cherrypy.request.json['data']['attributes']
        self._hostRepository.add_host(
            data['host'],
            data['hostname'],
            data['port'],
            data['username'],
            data['password']
        )
        return {'data': 'ADDED'}

    def PUT(self, name):
        data = cherrypy.request.json
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
