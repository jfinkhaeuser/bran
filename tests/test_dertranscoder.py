# -*- coding: utf-8 -*-
"""Test suite for cereal.DERTranscoder."""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2017 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()

import pytest

@pytest.fixture
def transcoder():
  from cereal import DERTranscoder
  return DERTranscoder()


@pytest.fixture
def nested_data():
  theset = set()
  theset.add(1)
  theset.add(2)
  theset.add(1)

  from collections import OrderedDict
  x = OrderedDict()
  x['baz'] = 42
  x['foo'] = 'bar'

  return {
    'set': theset,
    'none': None,
    'numbers': {
      'int': 42,
      'float': 3.1415,
      'complex': complex(1, -2),
    },
    'list': ['y', 'n'],
    'bools': (True, False),
    'strings': ("hällo",u"hällo",b"hallo"),
    'dict': x,
  }


def test_nested(transcoder, nested_data):
  decoded = transcoder.decode(transcoder.encode(nested_data))
  assert decoded == nested_data

