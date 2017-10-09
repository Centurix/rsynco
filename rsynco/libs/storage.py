from rsynco import Config


class Storage:
    """
    Storage class for hosts and jobs locally
    """
    def __init__(self):
        self.config = Config()

    def get_hosts(self):
        hosts = list()
        for host in self.config.data['hosts']:
            hosts.append({
                'host': host,
                'hostname': self.config.data['hosts'][host]['hostname'],
                'port': self.config.data['hosts'][host]['port'],
                'username': self.config.data['hosts'][host]['username'],
                'password': self.config.data['hosts'][host]['password']
            })
        return hosts

    def get_host(self, name):
        host = self.config.data['hosts'][name]
        return {
            'host': name,
            'hostname': host['hostname'],
            'port': host['port'],
            'username': host['username'],
            'password': host['password']
        }

    def add_host(self, host, hostname, port, username, password):
        self.config.data['hosts'][host] = {
            'host': host,
            'hostname': hostname,
            'port': port,
            'username': username,
            'password': password
        }
        return self.config.update()

    def update_host(self, host, hostname, port, username, password):
        self.config.data['hosts'][host]['hostname'] = hostname
        self.config.data['hosts'][host]['port'] = port
        self.config.data['hosts'][host]['username'] = username
        self.config.data['hosts'][host]['password'] = password
        return self.config.update()

    def delete_host(self, host):
        # Remove the host from the configuration file
        del self.config.data['hosts'][host]
        return self.config.update()

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
