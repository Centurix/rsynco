import cherrypy


class Activity(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"
