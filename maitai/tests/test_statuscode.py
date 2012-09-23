from unittest import TestCase

from webtest import TestApp

from webob import Response
from webob.dec import wsgify

from maitai.statuscode import StatusCodeRedirect

@wsgify
def bare_app(req):
    resp = Response('hello %s' % req.path_info)
    path = req.path_info[1:]
    if path.isdigit():
        resp.status = int(path)
    return resp


class TestStatusCodeRedirect(TestCase):

    def test_basic(self):
        app = TestApp(StatusCodeRedirect(bare_app))
        resp = app.get('/')
        resp.mustcontain('hello /')

        resp = app.get('/404', status=404)
        resp.mustcontain('hello /error/document')

    def test_custom(self):
        wrapped_app = StatusCodeRedirect(bare_app, errors=(400, 404),
                                         path='/handle')
        app = TestApp(wrapped_app)
        resp = app.get('/')
        resp.mustcontain('hello /')

        resp = app.get('/404', status=404)
        resp.mustcontain('hello /handle')

        resp = app.get('/403', status=403)
        resp.mustcontain('hello /403')
