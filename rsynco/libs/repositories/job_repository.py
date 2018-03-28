from .repository import Repository
import logging
from configobj import Section


class JobRepository(Repository):
    """
    Storage class for hosts and jobs locally
    """
    def get_job(self, name):
        logging.debug('REPOSITORY: Getting job {}'.format(name))
        job = self.config.data['jobs'][name]
        return {
            'name': name,
            'from_host': job['from_host'],
            'from_path': job['from_path'],
            'to_host': job['to_host'],
            'to_path': job['to_path'],
            'schedule': {
                'type': job['schedule']['type'],
                'day': job['schedule']['day'],
                'days': job['schedule']['days'],
                'date': job['schedule']['date'],
                'hour': job['schedule']['hour'],
                'minute': job['schedule']['minute'],
                'second': job['schedule']['second'],
                'secondFrequency': job['schedule']['secondFrequency'],
                'meridiem': job['schedule']['meridiem'],
                'week': job['schedule']['week'],
                'weekFrequency': job['schedule']['weekFrequency'],
                'month': job['schedule']['month'],
                'monthFrequency': job['schedule']['monthFrequency']
            }
        }

    def get_jobs(self):
        logging.debug('REPOSITORY: Getting all jobs')
        jobs = list()

        self.check_section('jobs')

        for job in self.config.data['jobs']:
            jobs.append({
                'name': job,
                'from_host': self.config.data['jobs'][job]['from_host'],
                'from_path': self.config.data['jobs'][job]['from_path'],
                'to_host': self.config.data['jobs'][job]['to_host'],
                'to_path': self.config.data['jobs'][job]['to_path'],
                'schedule': {
                    'type': self.config.data['jobs'][job]['schedule']['type'],
                    'day': self.config.data['jobs'][job]['schedule']['day'],
                    'days': self.config.data['jobs'][job]['schedule']['days'],
                    'date': self.config.data['jobs'][job]['schedule']['date'],
                    'hour': self.config.data['jobs'][job]['schedule']['hour'],
                    'minute': self.config.data['jobs'][job]['schedule']['minute'],
                    'second': self.config.data['jobs'][job]['schedule']['second'],
                    'secondFrequency': self.config.data['jobs'][job]['schedule']['secondFrequency'],
                    'meridiem': self.config.data['jobs'][job]['schedule']['meridiem'],
                    'week': self.config.data['jobs'][job]['schedule']['week'],
                    'weekFrequency': self.config.data['jobs'][job]['schedule']['weekFrequency'],
                    'month': self.config.data['jobs'][job]['schedule']['month'],
                    'monthFrequency': self.config.data['jobs'][job]['schedule']['monthFrequency']
                }
            })
        return jobs

    def add_job(self, name, from_host, from_path, to_host, to_path, schedule):
        logging.debug('REPOSITORY: Adding job {}'.format(name))

        self.check_section('jobs')

        self.config.data['jobs'][name] = {
            'name': name,
            'from_host': from_host,
            'from_path': from_path,
            'to_host': to_host,
            'to_path': to_path,
            'schedule': {
                'type': schedule['type'],
                'day': schedule['day'],
                'days': schedule['days'],
                'date': schedule['date'],
                'hour': schedule['hour'],
                'minute': schedule['minute'],
                'second': schedule['second'],
                'secondFrequency': schedule['secondFrequency'],
                'meridiem': schedule['meridiem'],
                'week': schedule['week'],
                'weekFrequency': schedule['weekFrequency'],
                'month': schedule['month'],
                'monthFrequency': schedule['monthFrequency']
            }
        }
        return self.config.update()

    def update_job(self, name, from_host, from_path, to_host, to_path, schedule):
        logging.debug('REPOSITORY: Updating job {}'.format(name))
        self.config.data['jobs'][name]['from_host'] = from_host
        self.config.data['jobs'][name]['from_path'] = from_path
        self.config.data['jobs'][name]['to_host'] = to_host
        self.config.data['jobs'][name]['to_path'] = to_path
        self.config.data['jobs'][name]['schedule'] = {
            'type': schedule['type'],
            'day': schedule['day'],
            'days': schedule['days'],
            'date': schedule['date'],
            'hour': schedule['hour'],
            'minute': schedule['minute'],
            'second': schedule['second'],
            'secondFrequency': schedule['secondFrequency'],
            'meridiem': schedule['meridiem'],
            'week': schedule['week'],
            'weekFrequency': schedule['weekFrequency'],
            'month': schedule['month'],
            'monthFrequency': schedule['monthFrequency']
        }
        return self.config.update()

    def delete_job(self, name):
        logging.debug('REPOSITORY: Deleting job {}'.format(name))
        del self.config.data['jobs'][name]
        return self.config.update()
