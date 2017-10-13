import cherrypy
from .apihandler import ApiHandler
from rsynco.libs.repositories.job_repository import JobRepository
from rsynco.libs.repositories.host_repository import HostRepository
from rsynco.libs.rsync import Rsync
from rsynco.libs.validation import validation
from rsynco.api.transformers.job_transformer import JobTransformer
import logging


class Jobs(ApiHandler):
    def __init__(self):
        self._JobRepository = JobRepository()
        self._HostRepository = HostRepository()
        self._Rsync = Rsync()

    def GET(self, name=None):
        if name is not None:
            logging.debug('API: Getting job {}'.format(name))
            return JobTransformer.jobs([self._JobRepository.get_job(name)])

        logging.debug('API: Listing all jobs')
        return JobTransformer.jobs(self._JobRepository.get_jobs())

    @validation
    def POST(self):
        data = cherrypy.request.json['data'][0]['attributes']
        logging.debug('API: Adding job {}'.format(data['name']))
        self._JobRepository.add_job(
            data['name'],
            data['from_host'],
            data['from_path'],
            data['to_host'],
            data['to_path']
        )
        cherrypy.response.status = 201
        return JobTransformer.jobs([data])

    @validation
    def PUT(self, name):
        data = cherrypy.request.json['data'][0]['attributes']
        logging.debug('API: Updating job {}'.format(name))
        self._JobRepository.update_job(
            name,
            data['from_host'],
            data['from_path'],
            data['to_host'],
            data['to_path']
        )
        return JobTransformer.jobs([data])

    def DELETE(self, name):
        logging.debug('API: Deleting job {}'.format(name))
        self._JobRepository.delete_job(name)
        return JobTransformer.empty_job()

    @validation
    def PATCH(self, name):
        data = cherrypy.request.json['data'][0]['attributes']
        logging.debug('API: Changing job state {}'.format(name))
        if data['status'] == 'start':
            job = self._JobRepository.get_job(name)
            logging.debug('API: Starting rsync from host {} to host {}'.format(job['from_host'], job['to_host']))

            self._Rsync.process(
                self._HostRepository.get_host(job['from_host']),
                job['from_path'],
                self._HostRepository.get_host(job['to_host']),
                job['to_path']
            )
        return JobTransformer.jobs([self._JobRepository.get_job(name)])
