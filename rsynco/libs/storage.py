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

    def update_host(self, host, hostname, port, username, password):
        # TODO: Update a specific host
        # TODO: Re-write the config file again
        # TODO: Split these out into classes for jobs/hosts etc?
        pass


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