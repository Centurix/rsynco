from .repository import Repository


class JobRepository(Repository):
    """
    Storage class for hosts and jobs locally
    """
    def get_job(self, name):
        job = self.config.data['jobs'][name]
        return {
            'name': name,
            'from_host': job['from_host'],
            'from_path': job['from_path'],
            'to_host': job['to_host'],
            'to_path': job['to_path']
        }

    def get_jobs(self):
        jobs = list()
        for job in self.config.data['jobs']:
            jobs.append({
                'name': job,
                'from_host': self.config.data['jobs'][job]['from_host'],
                'from_path': self.config.data['jobs'][job]['from_path'],
                'to_host': self.config.data['jobs'][job]['to_host'],
                'to_path': self.config.data['jobs'][job]['to_path']
            })
        return jobs

    def add_job(self, name, from_host, from_path, to_host, to_path):
        self.config.data['jobs'][name] = {
            'name': name,
            'from_host': from_host,
            'from_path': from_path,
            'to_host': to_host,
            'to_path': to_path
        }
        return self.config.update()

    def update_job(self, name, from_host, from_path, to_host, to_path):
        self.config.data['jobs'][name]['from_host'] = from_host
        self.config.data['jobs'][name]['from_path'] = from_path
        self.config.data['jobs'][name]['to_host'] = to_host
        self.config.data['jobs'][name]['to_path'] = to_path
        return self.config.update()

    def delete_job(self, name):
        del self.config.data['jobs'][name]
        return self.config.update()
