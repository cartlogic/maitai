Mai Tai - Handy WSGI Utilities
==============================

Scott Torborg - `Cart Logic <http://www.cartlogic.com>`_

Mai Tai is a collection of useful WSGI middlewares. The goal is to stand
alongside the excellent `Paste <http://pythonpaste.org>`_ and
`WebOb <http://webob.org>`_ libraries and provide tools that are handy for
practical WSGI application administration.


Installation
============

Install with pip::

    $ pip install maitai


Documentation
=============

Mai Tai has `extensive documentation here <http://www.cartlogic.com/maitai>`_.


To Do
=====

Additional tools that may be coming soon:

* Logging utilities.
* Request latency timing by request type.


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
