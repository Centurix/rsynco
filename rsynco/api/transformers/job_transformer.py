from datetime import date


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
                    'schedule': {
                        'type': job['schedule']['type'],
                        'day': job['schedule']['day'],
                        'days': job['schedule']['days'],
                        'date': job['schedule']['date'],
                        'hour': job['schedule']['hour'],
                        'minute': job['schedule']['minute'],
                        'second': job['schedule']['second'],
                        'secondFrequency': job['schedule']['secondFrequency'],
                        'meridiem': job['schedule']['meridiem'],
                        'week': job['schedule']['week'],
                        'weekFrequency': job['schedule']['weekFrequency'],
                        'month': job['schedule']['month'],
                        'monthFrequency': job['schedule']['monthFrequency']
                    }
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
                    'schedule': {
                        'type': 'none',
                        'day': 1,
                        'days': [],
                        'date': date.today().isoformat(),
                        'hour': 12,
                        'minute': 0,
                        'second': 0,
                        'secondFrequency': 10,
                        'meridiem': 'AM',
                        'week': 1,
                        'weekFrequency': 1,
                        'month': 1,
                        'monthFrequency': 1
                    }
                }
            }]
        }
