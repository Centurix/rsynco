from .apihandler import ApiHandler


class Jobs(ApiHandler):
    def GET(self):
        return {'data': []}
