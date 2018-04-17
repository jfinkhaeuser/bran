# -*- coding: utf-8 -*-
"""Test suite for bran.util."""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2017-2018 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()

import pytest

def test_stringify():
  from pyasn1.type.tag import Tag, TagSet
  from bran.util import stringify

  # First a single tag
  tag = Tag(0, 1, 2)
  assert '[0:1:2]' == stringify(tag)

  # Now a tag set with a single tag
  tagset = TagSet() + tag
  assert '[0:1:2]' == stringify(tagset)

  # With multiple tags
  tagset = TagSet() + tag + tag
  assert '[0:1:2]+[0:1:2]' == stringify(tagset)

  # With invalid value
  with pytest.raises(TypeError):
    stringify(None)

