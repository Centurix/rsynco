import cherrypy


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

    @staticmethod
    def nearest_path(path):
        # Return the 404 with the nearest path found
        cherrypy.response.status = 404

        return {
            'errors': [{
                "status": "404",
                "title": "Path not found, here's the closest valid path",
                "path": path
            }]
        }
