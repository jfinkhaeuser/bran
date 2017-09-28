|Build Status| |Docs| |License|
|PyPI| |Python Versions| |Package Format| |Package Status|


Bran provides transcoders for `ASN.1 <https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One>`__
serialization and deserialization, and `DER <https://en.wikipedia.org/wiki/X.690#DER_encoding>`__-encoding.

The purpose is to provide a serialization format for native Python types,
such as nested dicts, whose serialization is unambiguous and stable. That
is two values with the same contents serialize to the same byte string.

That makes it possible to create hashes and MACs to verify message
integrity.

Note that this does *not* make this package a full implementation of ``ASN.1``
specs. That is not the goal. The goal is just to have a stable byte
representation of Python values; ``DER`` in particular is only picked because
it helps in this.

Usage
=====

Code
----

You just encode some values. In most cases, you'll want to use the ``DERTranscoder``
class.

.. code:: python

    test = { 'some': { 'nested': 42, 'value': (0, 1, False) } }

    from bran import DERTranscoder
    transcoder = DERTranscoder()

    encoded = transcoder.encode(test)
    decoded = transcoder.decode(encoded)

    assert decoded == test

In order for bran to be this simple to use, some assumptions are made. The
one with the most impact is that *any* ``collections.Mapping`` will be encoded
to the same byte representation, which means when decoded, it will become a
Python ``dict``. Similar assumptions are made for ``collections.Set``
and ``collections.Sequence``.

For the purpose of hashing, consider the following code:

.. code:: python

    from bran.hash import hasher

    test = { 'some': { 'nested': 42, 'value': (0, 1, False) } }

    h = hasher()
    h.update(test)
    print(h.hexdigest())  # yields SHA512 hash of the DER serialized test

    import hashlib
    h = hasher(hashfunc = hashlib.md5)
    h.update(test)
    print(h.hexdigest())  # yields MD5 hash of the DER serialized test

Contributing
============

See `CONTRIBUTING.md <https://github.com/jfinkhaeuser/bran/blob/master/CONTRIBUTING.md>`__ for details.

License
=======

Licensed under MITNFA (MIT +no-false-attribs) License. See the
`LICENSE.txt <https://github.com/jfinkhaeuser/bran/blob/master/LICENSE.txt>`__ file for details.

.. |Build Status| image:: https://travis-ci.org/jfinkhaeuser/bran.svg?branch=master
   :target: https://travis-ci.org/jfinkhaeuser/bran
.. |Docs| image:: https://readthedocs.org/projects/pybran/badge/?version=latest
   :target: http://pybran.readthedocs.io/en/latest/
.. |License| image:: https://img.shields.io/pypi/l/bran.svg
   :target: https://pypi.python.org/pypi/bran/
.. |PyPI| image:: https://img.shields.io/pypi/v/bran.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/bran/
.. |Package Format| image:: https://img.shields.io/pypi/format/bran.svg
   :target: https://pypi.python.org/pypi/bran/
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/bran.svg
   :target: https://pypi.python.org/pypi/bran/
.. |Package Status| image:: https://img.shields.io/pypi/status/bran.svg
   :target: https://pypi.python.org/pypi/bran/
