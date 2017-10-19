from .apihandler import ApiHandler
from rsynco.api.transformers.path_transformer import PathTransformer
import logging
import os


class Paths(ApiHandler):
    def __init__(self):
        pass

    def GET(self, host=None, path=None):
        if host is None or path is None:
            logging.warning('API: Either host or path are missing, nothing returned')
            return PathTransformer.paths([])

        # Using the connection defails for {host}, retrieve the directory listing of {path}
        logging.debug('API: Getting path %s contents on server %s' % (path, host))
        contents = list()

        # localhost first
        for part in os.listdir(path):
            if os.path.isfile(os.path.join(path, part)):
                contents.append({
                    'name': part,
                    'type': 'file'
                })
            elif os.path.isdir(os.path.join(path, part)):
                contents.append({
                    'name': part,
                    'type': 'dir'
                })
            elif os.path.islink(os.path.join(path, part)):
                contents.append({
                    'name': part,
                    'type': 'link'
                })

        sorted_contents = sorted(contents, key=lambda x: x['type'] + ':' + x['name'].lower(), reverse=False)
        return PathTransformer.paths(sorted_contents)
