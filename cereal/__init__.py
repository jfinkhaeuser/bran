# -*- coding: utf-8 -*-
"""
Cereal provides DER-Encoded ASN.1 Serialization and Deserialization.

Other serialization methods abound, but DER-encoded ASN.1 is used in
cryptography for one particular reason: given the same object, its encoding
is the same, which means hashes over its encoded form are.

For much the same reason, DER-encoded ASN.1 is useful in other contexts.
"""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2017 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()
__version__ = '0.1.0'


class DERTranscoder(object):
  def __init__(self, inner):
    self.inner = inner

  def encode(self, value):
    from pyasn1.codec.der import encoder
    return encoder.encode(self.inner.encode(value))

  def decode(self, value):
    from pyasn1.codec.der import decoder
    decoded = decoder.decode(value)
    return self.inner.decode(decoded[0])


class ASN1Transcoder(object):

  from pyasn1.type import univ, tag, namedtype

  #: complex
  COMPLEX   = univ.Sequence(
                tagSet = univ.Sequence.tagSet.tagExplicitly(
                  tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0x01)
                )
              )
  #: collections.Sequence
  TUPLE     = univ.Sequence(
                tagSet = univ.Sequence.tagSet.tagExplicitly(
                  tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0x02)
                )
              )
  LIST      = univ.Sequence(
                tagSet = univ.Sequence.tagSet.tagExplicitly(
                  tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0x03)
                )
              )
  #: collections.Mapping
  MAPPING   = univ.Sequence(
                tagSet = univ.Sequence.tagSet.tagExplicitly(
                  tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0x04)
                )
              )
  #: collections.Set
  SET       = univ.Set(
                tagSet = univ.Set.tagSet.tagExplicitly(
                  tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0x05)
                )
              )


  def __init__(self, **kwargs):
    self.options = kwargs

  def encode(self, value):
    import six, collections
    from pyasn1.type import univ, char

    if value is None:
      return univ.Null()

    elif isinstance(value, bool):
      return univ.Boolean(value)

    elif isinstance(value, six.integer_types):
      return univ.Integer(value)

    elif isinstance(value, float):
      return univ.Real(value)

    elif isinstance(value, complex):
      return self.__encode_complex(value)

    elif isinstance(value, (bytes, bytearray)):
      return univ.OctetString(value)

    elif isinstance(value, six.text_type):
      return char.UTF8String(value.encode('utf8'))

    elif isinstance(value, six.binary_type):
      return univ.OctetString(bytearray(value))

    elif isinstance(value, collections.Mapping):
      return self.__encode_mapping(value)

    elif isinstance(value, collections.Set):
      return self.__encode_set(value)

    elif isinstance(value, collections.Sequence):
      return self.__encode_sequence(value)

    else:
      return self.__encode_from_registry(value)


  def __encode_from_registry(self, value):
    # TODO type registry
    raise TypeError('Cannot encode value of type "%s"!' % (type(value),))


  def __encode_complex(self, value):
    from pyasn1.type import univ, tag

    val = self.get_base(ASN1Transcoder.COMPLEX).clone()

    val.setComponentByPosition(0, self.encode(value.real))
    val.setComponentByPosition(1, self.encode(value.imag))

    return val


  def __encode_sequence(self, value):
    # Everything except for lists get coerced to a tuple
    base = ASN1Transcoder.TUPLE
    if isinstance(value, list):
      base = ASN1Transcoder.LIST
    val = self.get_base(base).clone()

    # Sequences can't be re-ordered
    for idx, item in enumerate(value):
      val.setComponentByPosition(idx, self.encode(item))

    return val


  def __encode_mapping(self, value):
    # coerce to dict
    val = self.get_base(ASN1Transcoder.MAPPING).clone()

    # Force ordering of keys by default
    keys = value.keys()
    if self.options.get('sort', True):
      keys = sorted(keys)

    for idx, key in enumerate(keys):
      val.setComponentByPosition(idx, self.encode((key, value[key])))

    return val


  def __encode_set(self, value):
    # Everything is a set
    val = self.get_base(ASN1Transcoder.SET).clone()

    # Force ordering of items by default
    items = value
    if self.options.get('sort', True):
      items = sorted(items)

    for idx, item in enumerate(items):
      val.setComponentByPosition(idx, self.encode(item))

    return val


  def decode(self, value):
    # import six, collections
    from pyasn1.type import univ, char

    if isinstance(value, univ.Null):
      return None

    elif isinstance(value, univ.Boolean):
      return bool(value)

    elif isinstance(value, univ.Integer):
      return int(value)

    elif isinstance(value, univ.Real):
      return float(value)

    elif isinstance(value, char.UTF8String):
      from six import text_type
      return text_type(value)

    elif isinstance(value, univ.OctetString):
      # FIXME? bytes? non-unicode string?
      from six import binary_type
      return binary_type(value)

    elif isinstance(value, univ.Sequence):
      # Look for sub type tags
      if value.isSameTypeWith(ASN1Transcoder.COMPLEX):
        # FIXME this is what we want; if this doesn't work, fix encoding order!
        return complex(
            self.decode(value.getComponentByPosition(0)),
            self.decode(value.getComponentByPosition(1))
        )

      if value.isSameTypeWith(ASN1Transcoder.TUPLE):
        return tuple(self.__sequence_iter(value))

      if value.isSameTypeWith(ASN1Transcoder.LIST):
        return list(self.__sequence_iter(value))

      if value.isSameTypeWith(ASN1Transcoder.MAPPING):
        ret = {}
        for key, value in self.__sequence_iter(value):
          ret[key] = value
        return ret

    elif isinstance(value, univ.Set):
      ret = set()
      for item in self.__sequence_iter(value):
        ret.add(item)
      return ret

  def __sequence_iter(self, seq):
    idx = 0
    while True:
      try:
        item = self.decode(seq.getComponentByPosition(idx))
        yield item
        idx += 1
      except IndexError:
        break


  def get_base(self, base):
    # TODO
    return base
    # bases = getattr(self.options, 'bases', {})
    # return bases.get(base, base)
