================
sphinx-no-pragma
================
.. External references

.. _Sphinx: https://github.com/sphinx-doc/sphinx
.. _jsphinx: https://jsphinx.readthedocs.io/
.. _MyPy: https://mypy.readthedocs.io/

.. Internal references

.. _sphinx-no-pragma: https://github.com/barseghyanartur/sphinx-no-pragma/
.. _Read the Docs: http://sphinx-no-pragma.readthedocs.io/
.. _Demo: http://sphinx-no-pragma.readthedocs.io/en/latest/demo.html
.. _Contributor guidelines: https://sphinx-no-pragma.readthedocs.io/en/latest/contributor_guidelines.html

**Improve developer experience**:

- Write better docs.
- Do not repeat yourself.
- Assure code low-maintenance.

.. image:: https://img.shields.io/pypi/v/sphinx-no-pragma.svg
   :target: https://pypi.python.org/pypi/sphinx-no-pragma.py
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/sphinx-no-pragma.svg
    :target: https://pypi.python.org/pypi/sphinx-no-pragma/
    :alt: Supported Python versions

.. image:: https://github.com/barseghyanartur/sphinx-no-pragma/actions/workflows/test.yml/badge.svg?branch=main
   :target: https://github.com/barseghyanartur/sphinx-no-pragma/actions
   :alt: Build Status

.. image:: https://readthedocs.org/projects/sphinx-no-pragma/badge/?version=latest
    :target: http://sphinx-no-pragma.readthedocs.io
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/barseghyanartur/sphinx-no-pragma/#License
   :alt: MIT

.. image:: https://coveralls.io/repos/github/barseghyanartur/sphinx-no-pragma/badge.svg?branch=main&service=github
    :target: https://coveralls.io/github/barseghyanartur/sphinx-no-pragma?branch=main
    :alt: Coverage

**TL;DR**

`sphinx-no-pragma`_ is a `Sphinx`_ extension for stripping pragma comments
from source code used in documentation.

If that's all you need to know to move forward, jump right to the
`installation`_. Otherwise, read further.

----

Some say, "documentation is the king". Others argue - "no, demos are". While
some say, "testing is everything!" and yet there will be someone else who
will jump in with "write clean code! black, isort, mypy and ruff everywhere!"

And yet there's you, who want to be good and write a better package, because
there's a generic problem that needs to be solved, and you know how, you want
to share it with the world. You also want to assure or at least make an effort
in making your project developer friendly, attractive for making contributions,
which eventually leads to continuous improvement and make it live long(er).

So, combining the best practices, you:

- Introduce examples in your repository to make it easier to start with.
- Write awesome docs with usage examples (by eventually repeating yourself,
  copying things from your actual code examples).
- Write tests for your code. Then you realize it's good to test the examples
  too. Eventually, you have now almost the same code in 3 places: tests,
  examples and docs.
- Introduce linters and `MyPy`_.

Then you invest your time in making sure all your code looks correct and fix
the never-ending `MyPy`_ issues.

Then you need to make a small change, which unfortunately, among other,
requires altering the examples code. You need to change the examples, the
docs, the tests and the examples tests. However, you also need to push the
change quickly. As many times before, you skip documentation update,
leaving it for "another time".

By that time you discover that code maintenance is a hell. You fix everything,
tests pass you're happy to push, by then `MyPy`_ starts to nag about issues
you have no idea how to solve and by that moment you don't care about them.
You're sick of it and start using pragma comments to silence the errors,
leaving the fix for another day. Your maintenance work involves a lot of
copy-pasting from one place to another (examples, tests, documentation).

Does this sound familiar?

----

What if I tell you that actually a couple of steps can be taken out.
Namely, that you can use your example code directly in your documentation,
using ``.. literalinclude::`` directive of `Sphinx`_. That part has already
been well covered in `jsphinx`_ project (JavaScript primarily). However,
what `jsphinx`_ didn't solve is presence of pragma comments in your
documentation. This project does take care of that part.
You don't need to choose or balance between readability, explainability and
low-maintenance.

Written by lazy developer for lazy developers to improve developer experience
in writing low-maintenance code.

Features
========
- Accurately stips out pragma comments from your source code that you include
  in your documentation.

Prerequisites
=============
Python 3.9+

Installation
============
.. code-block:: sh

    pip install sphinx-no-pragma

Documentation
=============
- Documentation is available on `Read the Docs`_.
- For guidelines on contributing check the `Contributor guidelines`_.

Usage example
=============
In order to move forward, you first need to get educate yourself a little on
`Sphinx`_'s directives. Namely the ``.. literalinclude::`` and ``:download:``.
For that, first read the `jsphinx`_ documentation.

But there might be a little problem with that. Of course you might be lucky and
have zero pragma comments in your code (no ``# noqa``,
no ``# type: ignore``, etc). But more often, you get at least a couple of
these. Your perfectionist nature doesn't easily allow you to let them be
part of your concise, beautiful documentation. Cursing me for earlier
advices, you start to replace your DRY documentation part with copy-pasted
examples.

This is where this package jumps in. It simply is a `Sphinx`_ extension that
strips all pragma comments from your code that goes into documentation.

Sphinx configuration
--------------------
Essential configuration
~~~~~~~~~~~~~~~~~~~~~~~
*Filename: docs/conf.py*

.. code-block:: python

    extensions = [
        # ... other extensions
        "sphinx_no_pragma",
        # ... other extensions
    ]

Fine-tuning what to strip
~~~~~~~~~~~~~~~~~~~~~~~~~
By default, the following markers are stripped:

- ``# type: ignore``
- ``# noqa``
- ``# pragma: no cover``
- ``# pragma: no branch``
- ``# fmt: off``
- ``# fmt: on``
- ``# fmt: skip``
- ``# yapf: disable``
- ``# yapf: enable``
- ``# pylint: disable``
- ``# pylint: enable``
- ``# flake8: noqa``
- ``# noinspection``
- ``# pragma: allowlist secret``
- ``# pragma: NOSONAR``

If you want to alter the default behaviour, define
a ``ignore_comments_endings`` variable in your Sphinx configuration
file (``docs/conf.py``) as shown below:

*Filename: docs/conf.py*

.. code-block:: python

    ignore_comments_endings = [
        "# type: ignore",
        "# noqa",
        "# pragma: no cover",
        "# pragma: no branch",
        "# fmt: off",
        "# fmt: skip",
        "# yapf: disable",
        "# pylint: disable",
        "# flake8: noqa",
        "# noinspection",
    ]

If you want to simply extend the list of markers, use another variable
to define your own list, that would be appended to the default one.

*Filename: docs/conf.py*

.. code-block:: python

    # Set user defined endings
    user_ignore_comments_endings = [
        "# [start]",
    ]

Code example
------------
*Filename: examples/example_1.py*

.. code-block:: python

    from typing import Any, Optional

    class ThirdPartyLibrary:
        @staticmethod
        def get_dynamic_object() -> Any:
            # Returns an object whose type is not known at compile time
            return "a string"  # In reality, this could be any type


    # Usage of the third-party library
    obj = ThirdPartyLibrary.get_dynamic_object()

    # Attempt to use the object as a string, even though its type is 'Any'
    length = len(obj)  # type: ignore

    # Deliberately long line to violate PEP 8 line length rule, suppressed with noqa
    print(f"The length of the object, a dynamically typed one, is just {length}")  # noqa

Given that this is your code structure:

.. code-block:: text

    ├── examples
    │  └── example_1.py
    ├── docs
    │  ├── conf.py
    │  ├── index.rst
    │  ├── Makefile
    │  ├── _static
    │  │  └── example_1.py
    │  └── usage.rst
    ├── LICENSE
    ├── Makefile
    ├── pyproject.toml
    ├── README.rst
    └── sphinx_no_pragma.py

Either use ``html_extra_path = ["examples"]`` or make a symlink to
``examples/example_1.py`` from ``docs/_static``.

Then include it in your docs as follows:

*Filename: example.rst*

.. code-block:: rst

    .. container:: jsphinx-download

    .. literalinclude:: _static/example_1.py
        :language: python
        :lines: 1-

    *See the full example*
    :download:`here <_static/example_1.py>`

Now, rendered, your code will not contain `# type: ignore` or `# noqa` pragma
comments.

See the `demo`_. Click on the `See the full example here` link to see
the original code.

Tests
=====
Run the tests with unittest:

.. code-block:: sh

    python -m unittest sphinx_no_pragma.py

Or pytest:

.. code-block:: sh

    pytest

License
=======
MIT

Support
=======
For security issues contact me at the e-mail given in the `Author`_ section.

For overall issues, go to
`GitHub <https://github.com/barseghyanartur/sphinx-no-pragma/issues>`_.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>
