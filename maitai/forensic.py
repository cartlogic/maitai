from time import time
from webob import Request
import simplejson as json


class ForensicMiddleware(object):
    """
    Log ALL request information as JSON, one request per line.

    NOTE: Needs to set some reasonable restrictions on request content length
    in order to be usable in production. Request bodies which are too large
    should be logged to a file, or truncated somehow.
    """
    def __init__(self, app, path):
        self.app = app
        self.f = open(path, 'a')

    def __call__(self, environ, start_response):
        req = Request(environ)
        resp = req.get_response(self.app)

        entry = dict(method=req.method,
                     body=req.body,
                     url=req.url,
                     time=time(),
                     headers=req.headers.items())
        line = json.dumps(entry)
        assert '\n' not in line
        self.f.write(line)
        self.f.write('\n')
        self.f.flush()

        return resp(environ, start_response)
