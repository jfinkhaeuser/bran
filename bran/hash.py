# -*- coding: utf-8 -*-
"""
This module provides a simple object hashing abstraction.

We use bran.DERTranscoder for serialization, and a hash function
from hashlib.
"""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2017-2018 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()

import hashlib


def hasher(obj = None, hashfunc = hashlib.sha512, *args, **kwargs):
  """
  Create a hashlib wrapper that hashes objects.

  The returned object implements `update`, `digest` and `hexdigest` like
  the hashblib hash functions. The difference is that instead of only
  accepting buffer API objects in `update`, any object that can be serialized
  using DERTranscoder is supported.

  :param mixed obj: An optional object to update the hash function with.
  :param callable hashfunc: One of hashlib's constructor functions; defaults to
    hashlib.sha512
  :return: A hashlib-like hasher.
  """
  class BranHasher(object):
    def __init__(self, obj, *args, **kwargs):
      # Initialize chosen hash function
      self.__hashfunc = hashfunc(*args, **kwargs)

      # Initialize transcoder
      from . import DERTranscoder
      self.__transcoder = DERTranscoder()

      # Start hashing if we've been given an object in the ctor
      if obj is not None:
        self.update(obj)

    def update(self, *args, **kwargs):
      # Replace args by encoded versions of its objects.
      encoded = [self.__transcoder.encode(x) for x in args]
      return self.__hashfunc.update(*encoded, **kwargs)

    def digest(self, *args, **kwargs):
      return self.__hashfunc.digest(*args, **kwargs)

    def hexdigest(self, *args, **kwargs):
      return self.__hashfunc.hexdigest(*args, **kwargs)

  return BranHasher(obj, *args, **kwargs)
