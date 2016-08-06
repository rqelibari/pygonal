Pygonal Overview
===============

Pygonal is a 2D geometry library for Python. It is a fork of [planar][11]
developed by Casey Duncan until 2011.
It is intended for use by games and interactive real-time applications,
but is designed to be useful for most any program that needs a convenient,
high-performance geometry API.

Pygonal is a standalone library and has no external dependencies besides
Python, and optionally a C compiler.

Pygonal is purely a math library, presentation, graphical or otherwise is
left up to the application.

[11]: <https://bitbucket.org/caseman/planar/> "Planar Repository"

Project Goals
-------------

* Do one thing, 2D geometry, and do it well.
* Provide a high-level, clean, Pythonic API.
* All APIs have both a Python reference implementation and a high performance
  implementation in C with the same interface.
* Compatibility with Python 2.6+, and Python 3.1+
* 100% test coverage.
* Full narrative and API reference documentation.
* Platform-independent.
* Be responsive to community input.

License
-------

Pygonal is distributed under the terms of the Apache 2.0 license.
For a complete text of the license see the ``LICENSE.txt`` file in the source
distrbution.

Acknowledgements
----------------

The API for Pygonal, and some of the code is derived from the excellent
work done by the [Super Effective Team][41] and [Casey Duncan][42], thanks guys!

[41]: http://www.supereffective.org/pages/Vector-2d-Vector-Library
[42]: https://github.com/caseman

Requirements
------------

Pygonal requires Python 2.6, 2.7, 3.1, or better.

To experience the exhilaration of native-code performance, a C compiler is
required. If someone volunteers, binary releases for platforms where this
is not common (you know who you are) will be happily made available.

Downloading Pygonal
------------------

Pygonal releases can be downloaded from the python package index (pypi):

* http://pypi.python.org/pypi/pygonal/

You can get the latest code in development from the Pygonal git
repository on github:

* https://github.com/rqelibari/pygonal/

Installation
------------

To build and install Pygonal from the source distribution or repository use::

    python setup.py install

To install only the pure-Python modules without compiling, use::

    python setup.py build_py install --skip-build

Only performance is sacrificed without the C extensions, all functionality is
still available when using only the pure-Python modules.

Tests
-----

Pygonal requires nose for testing. You can install it for Python 2.x
using easy_install::

    easy_install nose

For Python 3.x, you can download and install distribute from here:

* http://pypi.python.org/pypi/distribute

For now, you can get a copy of nose3 for Python 3.x, patched to install
properly on Python 3.1 here:

* http://bitbucket.org/caseman/nose3-caseman-fix/get/7c9181ad403d.zip

Once nose is installed you can run the tests from the source directory
using ``nosetests``, first building the C extensions, like so (on Unix)::

    python setup.py build && nosetests -d -w build/lib.*/pygonal/

This runs the tests inside the ``build`` directory so that the C extensions
can be tested. You can put a ``3`` suffix on the ``python`` and ``nosetests``
commands above for Python 3.x.

Documentation
-------------

You can browse the documentation online here:

* http://pygamesf.org/~casey/planar/doc/

The same documentation is also available for offline browsing in the
``doc/build/html`` subdirectory of the source distribution.

Contributing and Getting Support
--------------------------------

* *05 August 2016* More information is following.


