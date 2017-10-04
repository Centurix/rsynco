from rsynco.libs.daemon import Daemon
from rsynco.api.activity import Activity
from rsynco.api.hosts import Hosts
from rsynco.api.jobs import Jobs
from rsynco.api.root import Root

import os
import cherrypy

"""
To pause rsync, send the TSTP signal. Start rsync with --partial.
"""
# TODO: Cope with non-synco rsync jobs, we list them in actity but we cannot monitor progress
# TODO: Start/stop rsync jobs, send process output to /tmp somewhere with a predicable ID
# TODO: Store host and job details in a file somewhere
# TODO: Move server port to the configuration
# TODO: Validate JSON with JSON SCHEMA
# TODO: Refresh the activity page on an interval
# TODO: Make the burger menu work correctly on mobile
# TODO: Tests
# TODO: Better recovery from process hangs or failures in the daemon
# TODO: Make sure this is init.d/systemd/whatever friendly
# TODO: Include boilerplate for pip, pypi and other repositories
# TODO: Some kind of basic authentication
# TODO: Add a build process to pipelines and dump a release
# TODO: Host and Job entry pages
# TODO: Run rsync with --partial so we can pause and resume later


class RsyncoDaemon(Daemon):
    def __init__(self, pidfile):
        super().__init__(pidfile)
        self.root = os.path.join(os.path.dirname(__file__), "..", "web", "dist")

    def run(self):
        rest_config = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Access-Control-Allow-Origin', '*')]
            }
        }

        cherrypy.config.update({'server.socket_port': 8888})

        cherrypy.tree.mount(Activity(), '/activity', config=rest_config)
        cherrypy.tree.mount(Hosts(), '/hosts', config=rest_config)
        cherrypy.tree.mount(Jobs(), '/jobs', config=rest_config)
        cherrypy.tree.mount(Root(), '/', config={
            '/': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': self.root,
                'tools.staticdir.index': 'index.html'
            }
        })
        cherrypy.engine.start()
        cherrypy.engine.block()
