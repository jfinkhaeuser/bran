# -*- coding: utf-8 -*-
"""Test suite for cereal.ASN1Transcoder."""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2017 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()

import pytest

@pytest.fixture
def transcoder():
  from cereal import ASN1Transcoder
  return ASN1Transcoder()


def set_testing(transcoder, tag, values):
  for value in values:
    # Encoding must result in the expected tag set
    encoded = transcoder.encode(value)
    assert str(encoded.getTagSet()) == tag

    # Decoding must restore the value
    decoded = transcoder.decode(encoded)
    assert decoded == value

    # The value *type* must be derived from the decoded type (i.e. we can
    # lose some information here)
    assert isinstance(value, type(decoded))


def test_none(transcoder):
  set_testing(transcoder, '[0:0:5]', (None, ))


def test_boolean(transcoder):
  set_testing(transcoder, '[0:0:1]', (True, False))


def test_int(transcoder):
  set_testing(transcoder, '[0:0:2]', (-1, 0, 42, 2147483648))


def test_float(transcoder):
  set_testing(transcoder, '[0:0:9]', (-1.0, 0.0, 42.0, 2147483648.0))


def test_complex(transcoder):
  set_testing(transcoder, '[0:32:16]+[128:32:1]', (complex(1, 2), complex(complex(1, 2), -3.14)))


def test_binstr(transcoder):
  set_testing(transcoder, '[0:0:4]', ("test".encode('ascii'), ))


def test_bytes(transcoder):
  set_testing(transcoder, '[0:0:4]', (b'testvalue', ))


def test_text(transcoder):
  set_testing(transcoder, '[0:0:12]', (u"hello!", ))


def test_dict(transcoder):
  from collections import OrderedDict
  set_testing(transcoder, '[0:32:16]+[128:32:4]', ({1:2}, OrderedDict({1:2})))


def test_set(transcoder):
  val = set()
  val.add(1)
  val.add(2)
  set_testing(transcoder, '[0:32:17]+[128:32:5]', (val, ))


def test_tuple(transcoder):
  set_testing(transcoder, '[0:32:16]+[128:32:2]', ((1, 'a'), ))


def test_list(transcoder):
  set_testing(transcoder, '[0:32:16]+[128:32:3]', ([1, 'a'], ))


# TODO
# - nested types
# - dict without sorting
# - registry
