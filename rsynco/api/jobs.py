import cherrypy
from .apihandler import ApiHandler
from rsynco.libs.repositories.job_repository import JobRepository
from rsynco.libs.repositories.host_repository import HostRepository
from rsynco.libs.rsync import Rsync, NoHostException
from rsynco.libs.validation import validation
from rsynco.api.transformers.job_transformer import JobTransformer
import logging
from rsynco import job_queue


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
            data['to_path'],
            data['schedule']
        )
        cherrypy.response.status = 201
        logging.debug('API: Sending data to the QUEUE')
        job_queue.put(data['name'])
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
            data['to_path'],
            data['schedule']
        )
        logging.debug('API: Sending data to the QUEUE')
        job_queue.put(data['name'])
        return JobTransformer.jobs([data])

    def DELETE(self, name):
        logging.debug('API: Deleting job {}'.format(name))
        self._JobRepository.delete_job(name)
        # TODO: Delete the job from the scheduler
        return JobTransformer.empty_job()

    @validation
    def PATCH(self, name):
        data = cherrypy.request.json['data'][0]['attributes']
        logging.debug('API: Changing job state {}'.format(name))
        if data['status'] == 'start':
            job = self._JobRepository.get_job(name)
            logging.debug('API: Starting rsync from host {} to host {}'.format(job['from_host'], job['to_host']))

            try:
                self._Rsync.process(
                    self._HostRepository.get_host(job['from_host']),
                    job['from_path'],
                    self._HostRepository.get_host(job['to_host']),
                    job['to_path']
                )
            except NoHostException as no_host:
                logging.error(no_host)

        return JobTransformer.jobs([self._JobRepository.get_job(name)])
