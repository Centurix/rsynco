import cherrypy
from rsynco.libs.storage import Storage


class Hosts(object):
    exposed = True

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.tools.json_out(content_type='application/vnd.api+json')
    def GET(self, name=None):
        storage = Storage()

        if name is not None:
            return {'data': storage.get_host(name)}

        return {'data': storage.get_hosts()}
