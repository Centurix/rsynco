from .repository import Repository
from ..ssh import SshConfig
from pathlib import Path
import logging
import os


class HostRepository(Repository):
    """
    Storage class for hosts and jobs locally
    """

    def get_all_hosts(self):
        """
        Get all hosts available to rsync, both from the config file and also from
        the SSH config file
        :return:
        """
        logging.debug('REPOSITORY: Getting all hosts')
        hosts = list()
        # Add hosts from the SSH config file
        hosts.extend(self.get_system_ssh_config_hosts())
        hosts.extend(self.get_user_ssh_config_hosts())
        # Add hosts from the saved config file
        hosts.extend(self.get_hosts())
        return hosts

    def get_user_ssh_config_hosts(self):
        ssh_config_file = Path(str(os.path.expanduser('~/.ssh')), 'config')
        # ssh_config_file = Path(str(Path.home()), '.ssh', 'config')  # Python 3.5, Path.home()
        if ssh_config_file.is_file():
            ssh_config = SshConfig(ssh_config_file)
            return ssh_config.hosts

        return list()

    def get_system_ssh_config_hosts(self):
        # Just in case there are system wide defined hosts
        ssh_config_file = Path('/etc', 'ssh', 'ssh_config')
        if ssh_config_file.is_file():
            ssh_config = SshConfig(ssh_config_file)
            return ssh_config.hosts

        return list()

    def get_hosts(self):
        logging.debug('REPOSITORY: Getting rsynco hosts')
        hosts = list()

        self.check_section('hosts')

        for host in self.config.data['hosts']:
            hosts.append({
                'host': host,
                'hostname': self.config.data['hosts'][host]['hostname'],
                'port': self.config.data['hosts'][host]['port'],
                'username': self.config.data['hosts'][host]['username'],
                'password': self.config.data['hosts'][host]['password'],
                'type': 'rsynco'
            })
        return hosts

    def get_host(self, name):
        logging.debug('REPOSITORY: Getting host {}'.format(name))
        if name == 'localhost':
            return {
                'host': 'localhost',
                'hostname': 'localhost',
                'port': 22,
                'username': '',
                'password': '',
                'type': 'system'
            }

        hosts = self.get_all_hosts()

        host_index = next(index for (index, d) in enumerate(hosts) if d['host'] == name)

        if host_index < 0:
            return None

        return hosts[host_index]

    def add_host(self, host, hostname, port, username, password):
        logging.debug('REPOSITORY: Adding host {}'.format(host))

        self.check_section('hosts')

        self.config.data['hosts'][host] = {
            'host': host,
            'hostname': hostname,
            'port': port,
            'username': username,
            'password': password
        }
        return self.config.update()

    def update_host(self, host, hostname, port, username, password):
        logging.debug('REPOSITORY: Updating host {}'.format(host))
        self.config.data['hosts'][host]['hostname'] = hostname
        self.config.data['hosts'][host]['port'] = port
        self.config.data['hosts'][host]['username'] = username
        self.config.data['hosts'][host]['password'] = password
        return self.config.update()

    def delete_host(self, host):
        logging.debug('REPOSITORY: Deleting host {}'.format(host))
        # Remove the host from the configuration file
        del self.config.data['hosts'][host]
        return self.config.update()
