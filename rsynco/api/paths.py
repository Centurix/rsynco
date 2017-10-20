from .apihandler import ApiHandler
from rsynco.api.transformers.path_transformer import PathTransformer
import logging
from pathlib import Path
import psutil
from subprocess import PIPE
import re


class Paths(ApiHandler):
    def __init__(self):
        pass

    def GET(self, host=None, path=None):
        if host is None or path is None:
            logging.warning('API: Either host or path are missing, nothing returned')
            return PathTransformer.paths([])

        if host == "localhost":
            # Using the connection defails for {host}, retrieve the directory listing of {path}
            logging.debug('API: Getting path %s contents on server %s' % (path, host))
            contents = list()

            # Work our way up the tree till we find a valid path or root
            parsed_path = Path(path)

            logging.debug('Checking path %s' % path)
            if not parsed_path.exists():
                while not parsed_path.exists():
                    logging.debug('Path does not exist, working up the tree...')
                    logging.debug(parsed_path)
                    parsed_path = parsed_path.parent

                return PathTransformer.nearest_path(parsed_path.as_posix())

            # localhost first
            for part in parsed_path.iterdir():
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
        else:
            parsed_path = Path(path)

            contents = self.remote_listing(host, parsed_path.as_posix())

            if contents is None:
                while contents is None:
                    parsed_path = parsed_path.parent
                    contents = self.remote_listing(host, parsed_path.as_posix())

                return PathTransformer.nearest_path(parsed_path.as_posix())

        sorted_contents = sorted(contents, key=lambda x: x['type'] + ':' + x['name'].lower(), reverse=False)
        return PathTransformer.paths(sorted_contents)

    def remote_listing(self, host, path):
        """
        Clean this the fuck up. Works, but it's dodgy as.
        """
        logging.debug('Pulling a remote listing')
        p = psutil.Popen(['ssh', host, 'ls', '-F', path], stdout=PIPE, stderr=PIPE)

        main_output, main_error = p.communicate()

        error = main_error.decode(encoding='UTF-8')
        error_matched = re.search('No such file or directory', error)
        if error_matched is not None:
            logging.debug('PATH NOT FOUND, 404')
            return None

        logging.debug(main_error.decode(encoding='UTF-8'))
        results = main_output.decode(encoding='UTF-8').split("\n")

        contents = list()

        for line in results:
            logging.debug(line)
            if len(line) > 0:
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
