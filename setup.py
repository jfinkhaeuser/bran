#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dist utils for Bran.

This should work within tox, and install all required dependencies for testing.
"""

if __name__ == '__main__':
  # Get setup function
  try:
    from setuptools import setup, find_packages
  except ImportError:
    from distutils.core import setup, find_packages

  dev_require = [
    'tox>=2.8',
    'bump2version>=0.5',
    'pytest>=3.2',
    'pytest-cov>=2.5',
    'flake8>=3.4',
    'pep8-naming>=0.4',
    'flake8-quotes>=0.11',
    'flake8_docstrings>=1.1',
    'sphinx>=1.6',
  ]

  # Run setup
  setup(
      name = 'bran',
      version = '0.4.0',
      description = 'DER-Encoded ASN.1 Serialization and Deserialization',
      long_description = open('README.rst').read(),
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords = 'ASN.1 DER serialization',
      author = 'Jens Finkhaeuser',
      author_email = 'jens@finkhaeuser.de',
      url = 'https://github.com/jfinkhaeuser/bran',
      license = 'MITNFA',
      packages = find_packages(exclude = ['ez_setup', 'examples', 'tests']),
      include_package_data = True,
      install_requires = [
        'six~=1.11',
        'pyasn1~=0.4',
      ],
      extras_require = {
        'dev': dev_require,
      },
      scripts = [
      ],
      zip_safe = True,
      test_suite = 'tests',
      setup_requires = ['pytest-runner'],
      tests_require = dev_require,
  )
