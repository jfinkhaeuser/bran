# -*- coding: utf-8 -*-
"""Test suite for bran.ASN1Transcoder."""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2017 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()

import pytest

@pytest.fixture
def transcoder():
  from bran import ASN1Transcoder
  return ASN1Transcoder()

class Foo(object):
  def __eq__(self, other):
    return self.__dict__ == other.__dict__


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


def test_dict_sorting():
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

  # Default encoding will sort by keys, so would make the dicts equal
  from bran import ASN1Transcoder

  tc1 = ASN1Transcoder()
  x1 = tc1.encode(x)
  y1 = tc1.encode(y)
  assert x1 == y1

  # With sorting turned off, they should not be.
  tc2 = ASN1Transcoder(sort = False)
  x2 = tc2.encode(x)
  y2 = tc2.encode(y)
  assert x2 != y2

  # Try a sorting function. If we use an inverting function, y put
  # through the transcoder should equal x
  tc3 = ASN1Transcoder(sort = reversed)
  y3 = tc3.decode(tc3.encode(y))
  assert x == y3


def test_nested(transcoder, nested_data):
  decoded = transcoder.decode(transcoder.encode(nested_data))
  assert decoded == nested_data


def test_registry_basics():
  from bran import ASN1Transcoder

  test = { 'foo': Foo() }

  # Without a converter registry, we can't encode this
  with pytest.raises(TypeError):
    tc = ASN1Transcoder()
    encoded = tc.encode(test)

  from pyasn1.type import univ

  registry = {
    Foo: lambda x: univ.ObjectIdentifier([42]),
    '[0:0:6]': lambda x: Foo()
  }

  # With registry, we don't expect errors
  tc = ASN1Transcoder(registry = registry)
  encoded = tc.encode(test)

  # Decoding should fail without registry
  with pytest.raises(TypeError):
    tc1 = ASN1Transcoder()
    decoded = tc1.decode(encoded)

  # But with registry it must succeed
  decoded = tc.decode(encoded)
  assert decoded == test


def test_registry_no_callable():
  from bran import ASN1Transcoder

  registry = {
    Foo: 'not a callable',
    '[0:0:6]': 'not a callable',
  }
  tc = ASN1Transcoder(registry = registry)

  test = { 'foo': Foo() }
  with pytest.raises(ValueError):
    encoded = tc.encode(test)

  with pytest.raises(ValueError):
    from pyasn1.type import univ
    decoded = tc.decode(univ.ObjectIdentifier([42]))

