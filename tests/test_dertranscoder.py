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


def test_nested(transcoder, nested_data):
  decoded = transcoder.decode(transcoder.encode(nested_data))
  assert decoded == nested_data

