#!/usr/bin/env python

try:
  import os
  from setuptools import setup, find_packages
except ImportError:
  from distutils.core import setup

setup(
  name = 'pyquidnuncd',
  version = '0.0.1',
  author = 'Joseph Crail',
  author_email = 'jbcrail@gmail.com',
  description = "A blocking and streaming interface to quidnuncd",
  url = 'https://github.com/jbcrail/pyquidnuncd',
  license = 'MIT',
  install_requires = [],
  setup_requires = ['pytest-runner'],
  tests_require = ['pytest'],
  packages = find_packages(exclude=['contrib', 'docs']),
  scripts = ['bin/quidnuncd-cli'],

  classifiers = [
    'Intended Audience :: Developers',
    'Topic :: System :: Monitoring',
    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
  ],
  keywords = ['api', 'monitoring'],
)
