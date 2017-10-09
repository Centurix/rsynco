import cherrypy


@cherrypy.tools.accept(media='application/json')
@cherrypy.tools.json_out(content_type='application/vnd.api+json')
@cherrypy.tools.json_in()
class Jobs(object):
    exposed = True

    def GET(self):
        return {'data': []}
