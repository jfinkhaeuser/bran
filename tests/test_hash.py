# -*- coding: utf-8 -*-
"""Test suite for bran.hash."""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2017-2018 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()

import pytest

def test_hash():
  # OrderedDict keeps keys in insertion order, so the following two are
  # distinct.
  from collections import OrderedDict
  x = OrderedDict()
  x['foo'] = 'bar'
  x['baz'] = 42
  y = OrderedDict()
  y['baz'] = 42
  y['foo'] = 'bar'
  assert x != y

  # Hashing will sort keys, so the two hash digests must be the same.
  from bran.hash import hasher

  hx = hasher(x).hexdigest()
  hy = hasher(y).hexdigest()

  assert hx == hy

  hx = hasher(x).digest()
  hy = hasher(y).digest()

  assert hx == hy
