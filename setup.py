from setuptools import setup


setup(name="maitai",
      version='0.2',
      description='Handy WSGI Middleware Utilities',
      long_description='',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
          'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
      ],
      keywords='wsgi middleware cookies errors',
      url='http://github.com/cartlogic/maitai',
      author='Scott Torborg',
      author_email='scott@cartlogic.com',
      install_requires=[
          'webob',
      ],
      license='MIT',
      packages=['maitai'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
