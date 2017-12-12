from .repository import Repository
import logging


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
            'repeat': job['repeat'],
            'repeat_every': int(job['repeat_every'])
        }

    def get_jobs(self):
        logging.debug('REPOSITORY: Getting all jobs')
        jobs = list()

        if 'jobs' not in self.config.data.keys():
            return jobs

        for job in self.config.data['jobs']:
            jobs.append({
                'name': job,
                'from_host': self.config.data['jobs'][job]['from_host'],
                'from_path': self.config.data['jobs'][job]['from_path'],
                'to_host': self.config.data['jobs'][job]['to_host'],
                'to_path': self.config.data['jobs'][job]['to_path'],
                'repeat': self.config.data['jobs'][job]['repeat'],
                'repeat_every': int(self.config.data['jobs'][job]['repeat_every'])
            })
        return jobs

    def add_job(self, name, from_host, from_path, to_host, to_path, repeat, repeat_every):
        logging.debug('REPOSITORY: Adding job {}'.format(name))
        self.config.data['jobs'][name] = {
            'name': name,
            'from_host': from_host,
            'from_path': from_path,
            'to_host': to_host,
            'to_path': to_path,
            'repeat': repeat,
            'repeat_every': repeat_every
        }
        return self.config.update()

    def update_job(self, name, from_host, from_path, to_host, to_path, repeat, repeat_every):
        logging.debug('REPOSITORY: Updating job {}'.format(name))
        self.config.data['jobs'][name]['from_host'] = from_host
        self.config.data['jobs'][name]['from_path'] = from_path
        self.config.data['jobs'][name]['to_host'] = to_host
        self.config.data['jobs'][name]['to_path'] = to_path
        self.config.data['jobs'][name]['repeat'] = repeat
        self.config.data['jobs'][name]['repeat_every'] = repeat_every
        return self.config.update()

    def delete_job(self, name):
        logging.debug('REPOSITORY: Deleting job {}'.format(name))
        del self.config.data['jobs'][name]
        return self.config.update()
