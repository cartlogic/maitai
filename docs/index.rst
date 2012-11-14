Mai Tai - Handy WSGI Utilities
==============================

.. module:: maitai

Mai Tai is a collection of useful WSGI middlewares. The goal is to stand
alongside the excellent `Paste <http://pythonpaste.org>`_ and
`WebOb <http://webob.org>`_ libraries and provide tools that are handy for
practical WSGI application administration.

It is also:

* 40 mL white rum
* 20 mL dark rum
* 15 mL orange curacao
* 15 mL Orgeat syrup
* 10 mL fresh lime juice
* spear and lime peel garnish

Get the `code at GitHub <http://github.com/cartlogic/maitai>`_.


Installation
------------

The recommended installation method is pip.::

    pip install maitai

-------------------------------------


Track Git SCM version in request
--------------------------------

Tag requests with the current SHA1 hash of 1 or more git repositories.::

    from maitai.gitsha import GitSHAMiddleware

    app = SuperAwesomeApp()
    app = GitSHAMiddlware(app, '/opt/superawesome')

Inside your app code, you can access the SHA1 like::

    version = environ['git-sha1.superawesome']

-------------------------------------

Prevent app stack from sending secure cookies
---------------------------------------------

Intercept non-https requests and strip any ``Set-Cookie`` headers which set
cookies that are secure.

Useful for working around other misbehaving components which are leaking data
in your hybrid http/https deployment.::

    from maitai.securecookies import SecureCookiesMiddleware

    app = SlightlyLeakyStack()
    app = SecureCookiesMiddleware(app)

-------------------------------------

Rename cookies on the client
----------------------------

Look for a cookie by a certain name on the client, if it is present, rename it
to a new name and reset metadata to desired values.::

    from maitai.renamecookie import RenameCookieMiddleware

    app = App()
    app = RenameCookieMiddleware(app, 'old_cookie', 'new_cookie', secure=True)

This works by issuing an immediate 307 redirect in response to any requests
that have a cookie which matches 'old_cookie'.

Additional keyword arguments are available for setting all cookie metadata
attributes supported by WebOb's ``response.set_cookie()`` call, including
``expires``, ``max_age``, ``secure``, ``domain``, ``path``, ``httponly``, and
``comment``.

-------------------------------------

Prune cookies on the client
---------------------------

Prune all cookies from the client that either match a blacklist, or don't match
a whitelist.::

    from maitai.prunecookies import PruneCookiesMiddleware

    app = App()
    app = PruneCookiesMiddleware(app, whitelist=('session_id',
                                                 '__utma', '__utmb',
                                                 '__utmc', '__utmz'))

This works by issuing an immediate 307 redirect in response to any requests
that have a cookie that is "to be discarded".

.. note::

    As indicated above, regardless of your server-side code, don't forget that
    you may have 3rd-party javascript like Google Analytics which uses specific
    cookie names. Don't throw away your data!

-------------------------------------

Re-dispatch HTTP errors to a new request path
---------------------------------------------

Internally redirect a request based on status code. If a response has an HTTP
status which matches the list configured in the middleware, the request is
re-run with the URL path set to the configured path.

Inspired by the middleware that was included in Pylons, and shares the same
semantics, but rewritten for simplicity and to use WebOb.::

    from maitai.statuscode import StatusCodeRedirect

    app = SuperAwesomeApp()
    app = StatusCodeRedirect(app, errors=(400, 401, 403, 404, 500),
                             path='/error_handler')

Request re-issuing is non-recursive: the output of the second request will be
used no matter what it is.

-------------------------------------

Forensically log requests
-------------------------

Forensically log web requests. That is, log enough information about a web
request to make it possible to precisely reconstruct exactly what happened in
the request.

Logs request data as a JSON object per-line to an append-only file.::

    from maitai.forensic import ForensicMiddleware

    app = SuperAwesomeApp()
    app = ForensicMiddleware(app, '/var/log/maitai-forensic.log')

.. note::

    To Do:

    - Log the request handling time
    - Log the WSGI environ??
    - Log the response body, and the response headers.
    - Log timestamp in ISO 8601

-------------------------------------

.. include:: ../CHANGES

-------------------------------------

API
===

.. autoclass:: maitai.gitsha.GitSHAMiddleware
    :members:

.. autoclass:: maitai.securecookies.SecureCookiesMiddleware
    :members:

.. autoclass:: maitai.renamecookie.RenameCookieMiddleware
    :members:

.. autoclass:: maitai.prunecookies.PruneCookiesMiddleware
    :members:

.. autoclass:: maitai.statuscode.StatusCodeRedirect
    :members:

.. autoclass:: maitai.forensic.ForensicMiddleware
    :members:


License
=======

Mai Tai is licensed under an MIT license. Please see the LICENSE file for more
information.


Code Standards
==============

Mai Tai has a comprehensive test suite with 100% line and branch coverage, as
reported by the excellent ``coverage`` module. To run the tests, simply run in
the top level of the repo::

    $ nosetests

There are no `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_ or
`Pyflakes <http://pypi.python.org/pypi/pyflakes>`_ warnings in the codebase. To
verify that::

    $ pip install pep8 pyflakes
    $ pep8 .
    $ pyflakes .

Any pull requests must maintain the sanctity of these three pillars.
