import logging
from pathlib import Path
import psutil
from subprocess import PIPE
import re


class PathNotFoundException(Exception):
    def __init__(self, nearest_path=''):
        self.nearest_path = nearest_path


class SshConfig:
    """
    Parse SSH config files to their basic host details
    """
    def __init__(self, file):
        self.file = file
        self.hosts = list()
        self.parse()

    def new_host(self):
        return dict({'host': '', 'hostname': '', 'port': 22, 'username': '', 'password': '', 'type': 'system'})

    def parse(self):
        logging.debug('Parsing SSH config file {}'.format(str(self.file)))
        if not self.file.is_file():
            logging.debug('SSH config does not exist')
            return

        with self.file.open('r') as ssh_config:
            host = self.new_host()
            for line in ssh_config.readlines():
                stripped_line = line.strip(' \t\n')
                if stripped_line != '' and stripped_line[:1] != '#':
                    tokens = stripped_line.split()
                    if tokens[0].lower() == 'host' and len(tokens) > 1:
                        if host['host'] != '' and host['hostname'] != '':
                            self.hosts.append(host)
                        host = self.new_host()
                        host['host'] = tokens[1]
                    elif tokens[0].lower() == 'hostname' and len(tokens) > 1:
                        host['hostname'] = tokens[1]
                    elif tokens[0].lower() == 'port' and len(tokens) > 1:
                        host['port'] = int(tokens[1])
                    elif tokens[0].lower() == 'user' and len(tokens) > 1:
                        host['username'] = tokens[1]

            if host['host'] != '' and host['hostname'] != '':
                self.hosts.append(host)


class Ssh:
    def get_contents(self, host, path):
        parsed_path = Path(path)

        if host == "localhost":
            contents = self.local_listing(parsed_path)
        else:
            contents = self.remote_listing(host, parsed_path)

        return contents

    def local_listing(self, path):
        logging.debug('API: Getting local path %s contents' % path.as_posix())
        contents = list()

        # Work our way up the tree till we find a valid path or root
        logging.debug('Checking path %s' % path)
        if not path.exists():
            while not path.exists():
                logging.debug('Path does not exist, working up the tree...')
                logging.debug(path.as_posix())
                path = path.parent

            raise PathNotFoundException(path.as_posix())

        # localhost first
        for part in path.iterdir():
            if part.is_file():
                contents.append({
                    'name': part.name,
                    'type': 'file'
                })
            elif part.is_dir():
                contents.append({
                    'name': part.name,
                    'type': 'dir'
                })
            elif part.is_symlink():
                contents.append({
                    'name': part.name,
                    'type': 'link'
                })

        return contents

    def remote_exists(self, host, path):
        p = psutil.Popen(['ssh', host, 'ls', '-Fa', path.as_posix()], stdout=PIPE, stderr=PIPE)
        main_output, main_error = p.communicate()

        error = main_error.decode(encoding='UTF-8')
        error_matched = re.search('No such file or directory', error)

        if error_matched is not None:
            logging.debug('Path not found')
            return False
        else:
            return True

    def remote_iterdir(self, host, path):
        # Call out to the remote host
        p = psutil.Popen(['ssh', host, 'ls', '-Fa', path.as_posix()], stdout=PIPE, stderr=PIPE)
        main_output, main_error = p.communicate()

        logging.debug(main_error.decode(encoding='UTF-8'))
        return main_output.decode(encoding='UTF-8').split("\n")

    def remote_listing(self, host, path):
        logging.debug('API: Getting remote host %s path %s contents' % (host, path))
        contents = list()

        logging.debug('Checking path %s' % path)
        if not self.remote_exists(host, path):
            while not self.remote_exists(host, path):
                logging.debug('Path does not exist, working up the tree...')
                logging.debug(path.as_posix())
                path = path.parent

            raise PathNotFoundException(path.as_posix())

        for line in self.remote_iterdir(host, path):
            logging.debug(line)
            if len(line) > 0 and line != './' and line != '../':
                if line[-1] == '/':
                    contents.append({
                        'type': 'dir',
                        'name': line[:-1]
                    })
                elif line[-1] == '@':
                    contents.append({
                        'type': 'link',
                        'name': line[:-1]
                    })
                elif line[-1] == '*':
                    contents.append({
                        'type': 'file',
                        'name': line[:-1]
                    })
                elif line[-1] not in ['#']:
                    contents.append({
                        'type': 'file',
                        'name': line
                    })

        return contents
