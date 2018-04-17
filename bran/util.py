# -*- coding: utf-8 -*-
"""
Utility code for bran.

Contains a stringify function for tags/tagsets that does not include object
IDs, and thus becomes comparable.
"""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2017-2018 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()


def stringify(tag_or_tagset):
  """
  Return a string representation of a Tag or TagSet.

  Tag or TagSet are from pyasn1.type.tag.

  :param mixed tag_or_tagset: Either a Tag or a TagSet instance.
  :return: String representation.
  :raises: TypeError if the value is not a Tag or TagSet.
  """
  from pyasn1.type.tag import Tag, TagSet
  if isinstance(tag_or_tagset, Tag):
    return '[{0}:{1}:{2}]'.format(
        tag_or_tagset.tagClass,
        tag_or_tagset.tagFormat,
        tag_or_tagset.tagId)
  elif isinstance(tag_or_tagset, TagSet):
    return '+'.join(stringify(tag) for tag in tag_or_tagset)
  raise TypeError('{0} is not an instance of Tag or TagSet'.format(
      str(tag_or_tagset)))
