# -*- coding: utf-8 -*-
"""Dependency tests for bran."""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2017-2018 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()

import pytest

def test_pyasn1_version():
  from pyasn1 import __version__
  major, minor, patch = [int(x) for x in __version__.split('.')]
  assert major == 0
  assert minor >= 4
