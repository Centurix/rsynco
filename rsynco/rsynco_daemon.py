from rsynco.libs.daemon import Daemon
from rsynco.api.activity import Activity
from rsynco.api.hosts import Hosts
from rsynco.api.jobs import Jobs
from rsynco.api.root import Root
from rsynco import Config
import logging
import os
import cherrypy
from .scheduler import Scheduler


"""
To pause rsync, send the TSTP signal. Start rsync with --partial.
"""
# TODO: Validate job paths
# TODO: Add path explorer to job creation
# TODO: Create self-documenting API endpoints for blueprint
# TODO: Tests
# TODO: Make sure this is init.d/systemd/whatever friendly
# TODO: Include boilerplate for pip, pypi and other repositories
# TODO: Some kind of basic authentication
# TODO: Add a build process to pipelines and dump a release
# TODO: Use exceptions throughout
# TODO: Figure out how to pass the current server address to the SPA
# TODO: Force reload of ini settings for Jobs and Hosts in case another process changes them


class RsyncoDaemon(Daemon):
    def __init__(self, pidfile):
        super().__init__(pidfile)
        self.root = os.path.join(os.path.dirname(__file__), "..", "web", "dist")
        self._scheduler = Scheduler()

    def run(self):
        logging.debug('DAEMON SPAWNED')
        self.start_scheduler()
        config = Config()
        rest_config = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [
                    ('Access-Control-Allow-Origin', '*'),
                    ('Access-Control-Allow-Headers', 'Content-Type'),
                    ('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
                ]
            }
        }

        logging.debug('Init port and interface...')
        cherrypy.config.update({'server.socket_port': config.data['port'], 'server.socket_host': config.data['address']})

        logging.debug('Adding CherryPy endpoints...')
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

        logging.debug('Starting CherryPy...')
        cherrypy.engine.start()
        cherrypy.engine.block()

    def start_scheduler(self):
        logging.info('Spawning the scheduler')
        self._scheduler.start()
