class PathTransformer:
    @staticmethod
    def paths(contents):
        data_object = list()

        for item in contents:
            data_object.append({
                'type': 'paths',
                'id': item['name'],
                'attributes': {
                    'name': item['name'],
                    'type': item['type']
                }
            })

        return {
            'data': data_object
        }
