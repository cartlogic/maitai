from unittest import TestCase

from webtest import TestApp
from webob import Response
from webob.dec import wsgify

from maitai.securecookies import SecureCookiesMiddleware


@wsgify
def bare_app(req):
    resp = Response('ok')
    if req.params.get('cookie') in ('secure', 'both'):
        resp.set_cookie('foo', 'v', secure=True)
    if req.params.get('cookie') in ('insecure', 'both'):
        resp.set_cookie('bar', 'v', secure=False)
    if req.params.get('cookie') == 'nonwebob':
        resp.headers['Set-Cookie'] = 'baz=v; httponly; secure; Path=/;'
    return resp


wrapped_app = SecureCookiesMiddleware(bare_app)


class TestSecureCookies(TestCase):

    def assertHasCookie(self, resp, key):
        hdr = '\n'.join(resp.headers.getall('Set-Cookie'))
        self.assertIn("%s=" % key, hdr)

    def assertNotHasCookie(self, resp, key):
        hdr = '\n'.join(resp.headers.getall('Set-Cookie'))
        self.assertNotIn("%s=" % key, hdr)

    def test_bare_app_no_cookies_stripped(self):
        app = TestApp(bare_app)

        resp = app.get('/')
        self.assertNotHasCookie(resp, 'foo')
        self.assertNotHasCookie(resp, 'bar')

        resp = app.get('/?cookie=insecure')
        self.assertNotHasCookie(resp, 'foo')
        self.assertHasCookie(resp, 'bar')

        resp = app.get('/?cookie=secure')
        self.assertHasCookie(resp, 'foo')
        self.assertNotHasCookie(resp, 'bar')

        resp = app.get('/?cookie=both')
        self.assertHasCookie(resp, 'foo')
        self.assertHasCookie(resp, 'bar')

    def test_https_no_cookies_stripped(self):
        app = TestApp(wrapped_app)

        resp = app.get('https://localhost')
        self.assertNotHasCookie(resp, 'foo')
        self.assertNotHasCookie(resp, 'bar')

        resp = app.get('https://localhost?cookie=insecure')
        self.assertNotHasCookie(resp, 'foo')
        self.assertHasCookie(resp, 'bar')

        resp = app.get('https://localhost?cookie=secure')
        self.assertHasCookie(resp, 'foo')
        self.assertNotHasCookie(resp, 'bar')

        resp = app.get('https://localhost?cookie=both')
        self.assertHasCookie(resp, 'foo')
        self.assertHasCookie(resp, 'bar')

    def test_http_secure_cookie_stripped(self):
        app = TestApp(wrapped_app)

        resp = app.get('/')
        self.assertNotHasCookie(resp, 'foo')
        self.assertNotHasCookie(resp, 'bar')

        resp = app.get('/?cookie=insecure')
        self.assertNotHasCookie(resp, 'foo')
        self.assertHasCookie(resp, 'bar')

        resp = app.get('/?cookie=secure')
        self.assertNotHasCookie(resp, 'foo')
        self.assertNotHasCookie(resp, 'bar')

        resp = app.get('/?cookie=both')
        self.assertNotHasCookie(resp, 'foo')
        self.assertHasCookie(resp, 'bar')

    def test_nonwebob_format(self):
        app = TestApp(wrapped_app)

        resp = app.get('/')
        self.assertNotHasCookie(resp, 'baz')

        resp = app.get('/?cookie=nonwebob')
        self.assertNotHasCookie(resp, 'baz')

        resp = app.get('https://localhost?cookie=nonwebob')
        self.assertHasCookie(resp, 'baz')
