import os
from unittest import TestCase
from collections import defaultdict
from cgi import parse_qs

import simplejson as json

from webob import Response
from webob.dec import wsgify

from maitai.forensic import ForensicMiddleware

from .utils import FixedTestApp


@wsgify
def app(req):
    return Response('hello\nworld\ngoodbye\nworld')


class TestForensicMiddleware(TestCase):

    def setUp(self):
        self.path = '/tmp/maitai-forensic-test.log'
        if os.path.exists(self.path):
            os.remove(self.path)
        wrapped_app = ForensicMiddleware(app, self.path)
        self.app = FixedTestApp(wrapped_app)

    def file_contents(self):
        return open(self.path).read()

    def test_get_request_logging(self):
        self.app.get('/one', headers={'User-Agent': 'Awesomesauce'})
        self.app.get('/two')
        buf = self.file_contents()
        lines = buf.strip().split('\n')

        self.assertEqual(len(lines), 2)
        entry = json.loads(lines[0])

        self.assertEqual(entry['method'], 'GET')
        self.assertEqual(entry['url'], 'http://localhost/one')

        headers = defaultdict(list)
        for key, val in entry['headers']:
            headers[key].append(val)

        self.assertEqual(headers['User-Agent'], ['Awesomesauce'])

    def test_post_body_logging(self):
        self.app.post('/three',
                      {'pie': 'pumpkin',
                       'cake': 'red\nvelvet',
                       'pastry': 'croissant'},
                      headers={'User-Agent': 'Blorgify'})
        buf = self.file_contents()
        lines = buf.strip().split('\n')

        self.assertEqual(len(lines), 1)
        entry = json.loads(lines[0])

        self.assertEqual(entry['method'], 'POST')
        self.assertEqual(entry['url'], 'http://localhost/three')

        data = parse_qs(entry['body'])
        self.assertEqual(data['cake'], ['red\nvelvet'])
        self.assertEqual(data['pastry'], ['croissant'])
