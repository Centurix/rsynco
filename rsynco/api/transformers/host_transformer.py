class HostTransformer:
    @staticmethod
    def hosts(hosts):
        data_object = list()

        for host in hosts:
            data_object.append({
                'type': 'hosts',
                'id': host['host'],
                'attributes': {
                    'host': host['host'],
                    'hostname': host['hostname'],
                    'port': host['port'],
                    'username': host['username'],
                    'password': host['password'],
                    'type': host['type']
                }
            })

        return {
            'data': data_object
        }
