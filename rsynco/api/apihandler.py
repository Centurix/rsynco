import cherrypy


@cherrypy.tools.accept(media='application/json')
@cherrypy.tools.json_out(content_type='application/vnd.api+json')
@cherrypy.tools.json_in()
@cherrypy.expose
class ApiHandler(object):
    def OPTIONS(self, *args):
        return {'data': 'OK'}
