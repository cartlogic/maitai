from webtest import TestApp


class FixedTestApp(TestApp):
    """
    A patched version of webtest.TestApp which corrects a bug in which TestApp
    doesn't actually flush cookies which are deleted from the server (by a
    blank Set-Cookie call).
    """
    def prune_empty_cookies(self):
        for cookie, value in list(self.cookies.items()):
            if value == '':
                del self.cookies[cookie]

    def do_request(self, req, status, expect_errors):
        ret = TestApp.do_request(self, req, status, expect_errors)
        self.prune_empty_cookies()
        return ret
