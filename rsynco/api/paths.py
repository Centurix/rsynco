from .apihandler import ApiHandler
from rsynco.api.transformers.path_transformer import PathTransformer
import logging
from rsynco.libs.ssh import PathNotFoundException
from rsynco.libs.ssh import Ssh


class Paths(ApiHandler):
    def __init__(self):
        pass

    def GET(self, host=None, path=None):
        if host is None or path is None:
            logging.warning('API: Either host or path are missing, nothing returned')
            return PathTransformer.paths([])

        try:
            ssh = Ssh()
            contents = ssh.get_contents(host, path)
            sorted_contents = sorted(contents, key=lambda x: x['type'] + ':' + x['name'].lower(), reverse=False)
            return PathTransformer.paths(sorted_contents)
        except PathNotFoundException as e:
            return PathTransformer.nearest_path(e.nearest_path)
