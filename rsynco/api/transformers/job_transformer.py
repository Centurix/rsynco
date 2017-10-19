class JobTransformer:
    @staticmethod
    def jobs(jobs):
        data_object = list()

        for job in jobs:
            data_object.append({
                'type': 'jobs',
                'id': job['name'],
                'attributes': {
                    'name': job['name'],
                    'from_host': job['from_host'],
                    'from_path': job['from_path'],
                    'to_host': job['to_host'],
                    'to_path': job['to_path'],
                    'repeat': job['repeat'],
                    'repeat_every': job['repeat_every']
                }
            })

        return {
            'data': data_object
        }

    @staticmethod
    def empty_job():
        return {
            'data': [{
                'type': 'jobs',
                'attributes': {
                    'name': '',
                    'from_host': '',
                    'from_path': '',
                    'to_host': '',
                    'to_path': '',
                    'repeat': '',
                    'repeat_every': 1
                }
            }]
        }
