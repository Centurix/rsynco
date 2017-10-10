class SshConfig:
    """
    Parse SSH config files to their basic host details
    """
    def __init__(self, file):
        self.file = file
        self.hosts = list()
        self.parse()

    def parse(self):
        """
        Parse the current file
        :return:
        """
        with self.file.open('r') as ssh_config:
            host = dict({'host': '', 'hostname': '', 'port': 22, 'username': '', 'password': '', 'type': 'system'})
            for line in ssh_config.readlines():
                stripped_line = line.strip(' \t\n').lower()
                if stripped_line != '' and stripped_line[:1] != '#':
                    tokens = stripped_line.split()
                    if tokens[0] == 'host' and len(tokens) > 1:
                        if tokens[1][:1] != '-' and host['host'] != '' and host['hostname'] != '':
                            self.hosts.append(host)
                        host = dict({'host': '', 'hostname': '', 'port': 22, 'username': '', 'password': '', 'type': 'system'})
                        host['host'] = tokens[1]
                    elif tokens[0] == 'hostname' and len(tokens) > 1:
                        host['hostname'] = tokens[1]
                    elif tokens[0] == 'port' and len(tokens) > 1:
                        host['port'] = int(tokens[1])
                    elif tokens[0] == 'user' and len(tokens) > 1:
                        host['username'] = tokens[1]

            if host['host'] != '' and host['hostname'] != '':
                self.hosts.append(host)
