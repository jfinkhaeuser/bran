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
  """
  DER-encode Python builtin (and extended) types.

  The class first uses ASN1Transcoder to encode valuesin ASN.1 classes, then
  DER-encodes the result.
  """

  def __init__(self, inner = None):
    """
    Initialize DERTranscoder.

    The sole parameter is a reference to an inner decoder. If not specified,
    this defaults to an ASN1Transcoder instance with default options.

    :param object inner: [optional] Inner transcoder
    """
    self.inner = inner or ASN1Transcoder()

  def encode(self, value):
    """
    DER-encode the given value.

    Nested values are encoded recursively.

    :param mixed value: The value to encode.
    :return: An DER-encoded ASN.1 value, i.e. a byte sequence.
    """
    from pyasn1.codec.der import encoder
    return encoder.encode(self.inner.encode(value))

  def decode(self, value):
    """
    DER-deocde the given byte sequence.

    :param bytes value: The value to decode.
    :return: A Python value, the result of passing the parameter through DER
        decoding and ASN.1 decoding.
    """
    from pyasn1.codec.der import decoder
    decoded = decoder.decode(value)
    return self.inner.decode(decoded[0])


class ASN1Transcoder(object):
  """
  Transcode Python builtin (and extended) types to and from ASN.1 classes.

  Note that encoding is lossy with regards to specialized types.

  For many Python builtin types, there are corresponding universal ASN.1 data
  types available.

  For tuple() and list(), we use explicit tagging (which, when DER-encoded,
  takes up a few extra Bytes of space) to disambiguate one kind of sequence
  from another. Any collections.Sequence that is not specifically a list is
  encoded as a tuple(), any additional type information.

  Similarly, any collections.Mapping is encoded in the same way, and so is
  any collections.Set. If you use special subtypes of these Abstract Base
  Classes, that type information is lost.

  Still, it means that any nested structure will result in an equality-
  comparable nested structure, which is all that often times is required.
  """

  from pyasn1.type import univ, tag, namedtype

  #: Tags for complex
  COMPLEX = univ.Sequence(
    tagSet = univ.Sequence.tagSet.tagExplicitly(
      tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0x01)
    )
  )
  #: Tags for collections.Sequence
  TUPLE = univ.Sequence(
    tagSet = univ.Sequence.tagSet.tagExplicitly(
      tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0x02)
    )
  )
  LIST = univ.Sequence(
    tagSet = univ.Sequence.tagSet.tagExplicitly(
      tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0x03)
    )
  )
  #: Tags for collections.Mapping
  MAPPING = univ.Sequence(
    tagSet = univ.Sequence.tagSet.tagExplicitly(
      tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0x04)
    )
  )
  #: Tags for collections.Set
  SET = univ.Set(
    tagSet = univ.Set.tagSet.tagExplicitly(
      tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0x05)
    )
  )

  def __init__(self, **kwargs):
    """
    Initialize the transcoder.

    Keyword arguments are stored as options. Some such recognized options are:

    :param bool sort: Either a key sorting function, or False. If False, no
        sorting is performed. The default is to perform key sorting using the
        sorted() function.
    """
    self.options = kwargs

  def encode(self, value):
    """
    Encode the given Python value.

    Nested values (for Sequence, Set and Mapping) are recursively encoded.

    :param mixed value: The value to encode.
    :return: An ASN.1 class encapsulating the value.
    """
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

    elif isinstance(value, (bytes, bytearray, six.binary_type)):
      return univ.OctetString(bytearray(value))

    elif isinstance(value, six.text_type):
      return char.UTF8String(value.encode('utf8'))

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
    # Encode complex() values
    val = ASN1Transcoder.COMPLEX.clone()

    val.setComponentByPosition(0, self.encode(value.real))
    val.setComponentByPosition(1, self.encode(value.imag))

    return val

  def __encode_sequence(self, value):
    # Everything except for lists get coerced to a tuple
    base = ASN1Transcoder.TUPLE
    if isinstance(value, list):
      base = ASN1Transcoder.LIST
    val = base.clone()

    # Sequences can't be re-ordered
    for idx, item in enumerate(value):
      val.setComponentByPosition(idx, self.encode(item))

    return val

  def __encode_mapping(self, value):
    # coerce to dict
    val = ASN1Transcoder.MAPPING.clone()

    # Force ordering of keys by default
    keys = value.keys()
    sorter = self.options.get('sort', sorted)
    if sorter is not False:
      keys = sorter(keys)

    for idx, key in enumerate(keys):
      val.setComponentByPosition(idx, self.encode((key, value[key])))

    return val

  def __encode_set(self, value):
    # Everything is a set
    val = ASN1Transcoder.SET.clone()

    # Force ordering of items by default
    items = value
    sorter = self.options.get('sort', sorted)
    if sorter is not False:
      items = sorter(items)

    for idx, item in enumerate(items):
      val.setComponentByPosition(idx, self.encode(item))

    return val

  def decode(self, value):
    """
    Decode the given ASN.1 class into a Python value.

    Nested values (for Sequence, Set and Mapping) are recursively decoded.

    :param mixed value: The value to decode.
    :return: An Python value.
    """
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

    else:
      raise TypeError("Can't decode!")  # FIXME registry

  def __sequence_iter(self, seq):
    # Iterate through a univ.Sequence, decode and yield each item
    idx = 0
    while True:
      try:
        item = self.decode(seq.getComponentByPosition(idx))
        yield item
        idx += 1
      except IndexError:
        break
