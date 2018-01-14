class ActivityTransformer:
    @staticmethod
    def activities(activities):
        data_object = list()

        for activity in activities:
            data_object.append({
                'type': 'activities',
                'attributes': {
                    'pid': activity['pid'],
                    'started': activity['started'],
                    'from': activity['from'],
                    'to': activity['to'],
                    'progress': activity['progress'],
                    'status': activity['status'],
                    'type': activity['type']
                }
            })

        return {
            'data': data_object
        }
