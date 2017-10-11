import cherrypy
from .apihandler import ApiHandler
from rsynco.libs.repositories.job_repository import JobRepository
from rsynco.libs.validation import validation
from rsynco.api.transformers.job_transformer import JobTransformer


class Jobs(ApiHandler):
    def __init__(self):
        self._JobRepository = JobRepository()

    def GET(self, name=None):
        if name is not None:
            return JobTransformer.jobs([self._JobRepository.get_job(name)])

        return JobTransformer.jobs(self._JobRepository.get_jobs())

    @validation
    def POST(self):
        data = cherrypy.request.json['data'][0]['attributes']
        self._JobRepository.add_job(
            data['name'],
            data['from_host'],
            data['from_path'],
            data['to_host'],
            data['to_path']
        )
        return {'data': 'ADDED'}

    @validation
    def PUT(self, name):
        data = cherrypy.request.json['data'][0]['attributes']
        self._JobRepository.update_job(
            name,
            data['from_host'],
            data['from_path'],
            data['to_host'],
            data['to_path']
        )
        return {'data': 'UPDATED'}

    def DELETE(self, name):
        self._JobRepository.delete_job(name)
        return {'data': 'DELETED'}
