from unittest import TestCase

from webob import Response
from webob.dec import wsgify
from webtest import TestApp

from maitai.renamecookie import RenameCookieMiddleware


@wsgify
def bare_app(req):
    s = '\n'.join(['%s: %s' % (k, v)
                   for k, v in req.cookies.iteritems()])
    resp = Response(s)

    key = req.path_info_pop()
    if key:
        val = req.path_info_pop()
        resp.set_cookie(key, val)

    return resp


class FixedTestApp(TestApp):
    """
    A patched version of webtest.TestApp which corrects a bug in which TestApp
    doesn't actually flush cookies which are deleted from the server (by a
    blank Set-Cookie call).
    """
    def prune_empty_cookies(self):
        for cookie, value in self.cookies.items():
            if value == '':
                del self.cookies[cookie]

    def do_request(self, req, status, expect_errors):
        ret = TestApp.do_request(self, req, status, expect_errors)
        self.prune_empty_cookies()
        return ret


class TestRenameCookieMiddleware(TestCase):

    def test_basic(self):
        wrapped_app = RenameCookieMiddleware(bare_app, 'first', 'second')
        app = FixedTestApp(wrapped_app)

        resp = app.get('/first/blah')
        self.assertEqual(resp.body, '')

        resp = app.get('/', status=307)
        resp = resp.follow()
        self.assertEqual(resp.body, 'second: blah')

    def test_with_metadata(self):
        wrapped_app = RenameCookieMiddleware(bare_app, 'ewok', 'jedi',
                                             secure=True, httponly=True)
        app = FixedTestApp(wrapped_app)

        resp = app.get('/ewok/hello')
        self.assertEqual(resp.body, '')
        headers = resp.headers.getall('Set-Cookie')
        self.assertEqual(len(headers), 1)
        self.assertNotIn('Secure;', headers[0])
        self.assertNotIn('HttpOnly;', headers[0])

        resp = app.get('/', status=307)
        headers = resp.headers.getall('Set-Cookie')
        for hdr in headers:
            if 'jedi' in hdr:
                self.assertIn('secure', hdr)
                self.assertIn('HttpOnly', hdr)
            else:
                self.assertIn('ewok', hdr)

        resp = resp.follow()
        self.assertEqual(resp.body, 'jedi: hello')
