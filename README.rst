|Build Status| |PyPI| |Docs|

Bran provides transcoders for `ASN.1 <https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One>`__
serialization and deserialization, and `DER <https://en.wikipedia.org/wiki/X.690#DER_encoding>`__-encoding.

The purpose is to provide a serialization format for native Python types,
such as nested dicts, whose serialization is unambiguous and stable, that
is two values with the same contents serialize to the same byte string.

That makes it possible to create hashes and MACs to verify message
integrity.

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
one with the most impact is that it treats *any* ``collections.Mapping`` will
be encoded to the same byte representation, which means when decoded, it will
become a Python ``dict``. Similar assumptions are made for ``collections.Set``
and ``collections.Sequence``.

Setup
-----

Use
`virtualenv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`__
to create a virtual environment and change to it or not, as you see fit.

Then install the requirements:

.. code:: bash

    $ pip install -r requirements.txt

Documentation
-------------

After setup, run the following to generate documentation:

.. code:: bash

    $ python setup.py build_sphinx

Development
-----------

Test Execution
~~~~~~~~~~~~~~

Run the whole test suite:

.. code:: bash

    $ python setup.py test

Run a single test scenario:

.. code:: bash

    $ pytest tests/test_asn1transcoder.py::test_none

Run tests on multiple Python versions:

.. code:: bash

    $ tox

Run tests on Python 2.7:

.. code:: bash

    $ tox -e py27

A simple test coverage report is automatically generated.

License
=======

Licensed under MITNFA (MIT +no-false-attribs) License. See the
`LICENSE.txt <https://github.com/jfinkhaeuser/bran/blob/master/LICENSE.txt>`__ file for details.

.. |Build Status| image:: https://travis-ci.org/jfinkhaeuser/bran.svg?branch=master
   :target: https://travis-ci.org/jfinkhaeuser/bran
.. |PyPI| image:: https://img.shields.io/pypi/v/bran.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/bran/
.. |Docs| image:: https://readthedocs.org/projects/pybran/badge/?version=latest
   :target: http://pybran.readthedocs.io/en/latest/
