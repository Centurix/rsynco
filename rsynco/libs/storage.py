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

"""
We have an INI file already, use that.
[Host]
    [[Host name]]
        hostname
        port
        user
        password
[Job]
    [[Job name]]
        from
        to
        start
"""