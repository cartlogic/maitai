import os
import os.path
import subprocess
import shutil
from unittest import TestCase, skipUnless

from webtest import TestApp
from webob import Response
from webob.dec import wsgify

from maitai.gitsha import GitSHAMiddleware


git_path = None
for path in os.environ['PATH'].split(os.pathsep):
    fpath = os.path.join(path, 'git')
    if os.path.exists(fpath) and os.access(fpath, os.X_OK):
        git_path = fpath


@wsgify
def bare_app(req):
    repos = ['%s: %s' % (key, val)
             for key, val in req.environ.items()
             if key.startswith('git-sha1.')]
    return Response('\n'.join(repos))


class working_dir(object):
    def __init__(self, dir):
        self.dir = dir

    def __enter__(self):
        self.orig_dir = os.getcwd()
        os.chdir(self.dir)

    def __exit__(self, type, value, traceback):
        os.chdir(self.orig_dir)


class MockGitRepo(object):

    def __init__(self, path):
        self.path = path

    def init(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

        os.mkdir(self.path)
        null = open('/dev/null', 'w')
        subprocess.call([git_path, 'init'], cwd=self.path, stdout=null)

    def commit(self):
        with open(os.path.join(self.path, 'somefile'), 'a') as f:
            f.write('blah\n')

        null = open('/dev/null', 'w')
        subprocess.call([git_path, 'add', 'somefile'], cwd=self.path,
                        stdout=null)
        subprocess.call([git_path, 'commit', '-m', 'blah'], cwd=self.path,
                        stdout=null)
        sha1 = subprocess.check_output([git_path, 'log', '-1',
                                        '--pretty=format:%H'], cwd=self.path)
        return sha1


class TestGitSHAMiddleware(TestCase):

    def test_nonexistent_repo(self):
        app = TestApp(GitSHAMiddleware(bare_app, '/tmp/nonexistent-hopefully'))
        resp = app.get('/')
        resp.mustcontain("git-sha1.nonexistent-hopefully: "
                         "[Errno 2] No such file or directory: "
                         "'/tmp/nonexistent-hopefully/.git/HEAD'")

    @skipUnless(git_path, "git executable not found in $PATH")
    def test_commits(self):
        repo = MockGitRepo('/tmp/maitai-test-git-repo')
        repo.init()
        sha1 = repo.commit()

        app = TestApp(GitSHAMiddleware(bare_app, repo.path))
        resp = app.get('/')
        self.assertEqual(resp.body, b'git-sha1.maitai-test-git-repo: ' + sha1)
