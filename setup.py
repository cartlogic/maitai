from setuptools import setup


setup(name="maitai",
      version='0.1',
      description='',
      long_description='',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
      ],
      keywords='',
      author='Scott Torborg',
      author_email='scott@cartlogic.com',
      install_requires=[
          'webob',
          # These are for tests.
          'coverage',
          'nose>=1.1',
          'nose-cover3',
          'webtest',
      ],
      license='MIT',
      packages=['maitai'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
