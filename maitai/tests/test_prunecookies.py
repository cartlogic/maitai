from unittest import TestCase

from webob import Response
from webob.dec import wsgify

from maitai.prunecookies import PruneCookiesMiddleware

from .utils import FixedTestApp


@wsgify
def bare_app(req):
    s = '\n'.join(['%s: %s' % (k, v)
                   for k, v in req.cookies.items()])
    return Response(s)


class TestPruneCookiesMiddleware(TestCase):

    def test_whitelist(self):
        wrapped_app = PruneCookiesMiddleware(bare_app,
                                             whitelist=('foo', 'bar', 'baz'))
        app = FixedTestApp(wrapped_app)

        resp = app.get('/')
        self.assertEqual(resp.body, b'')

        app.cookies = {
            'foo': '123',
            'bar': '456',
            'baz': '789',
            'quux': '111',
            'larry': '222',
            'curly': '333',
            'moe': '444',
        }

        resp = app.get('/', status=307)
        resp = resp.follow()
        resp.mustcontain('foo: 123')
        resp.mustcontain('bar: 456')
        resp.mustcontain('baz: 789')

        body = resp.body.decode('utf-8')
        self.assertNotIn('quux', body)
        self.assertNotIn('larry', body)
        self.assertNotIn('curly', body)
        self.assertNotIn('moe', body)

    def test_blacklist(self):
        wrapped_app = PruneCookiesMiddleware(bare_app,
                                             blacklist=('quux', 'larry',
                                                        'curly', 'moe'))
        app = FixedTestApp(wrapped_app)

        resp = app.get('/')
        self.assertEqual(resp.body, b'')

        app.cookies = {
            'foo': '123',
            'bar': '456',
            'baz': '789',
            'quux': '111',
            'larry': '222',
            'curly': '333',
            'moe': '444',
        }

        resp = app.get('/', status=307)
        resp = resp.follow()
        resp.mustcontain('foo: 123')
        resp.mustcontain('bar: 456')
        resp.mustcontain('baz: 789')

        body = resp.body.decode('utf-8')
        self.assertNotIn('quux', body)
        self.assertNotIn('larry', body)
        self.assertNotIn('curly', body)
        self.assertNotIn('moe', body)
