import cherrypy
from rsynco.libs.storage import Storage


class Hosts(object):
    exposed = True

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.tools.json_out(content_type='application/vnd.api+json')
    def GET(self):
        storage = Storage()
        return {'data': storage.get_hosts()}
