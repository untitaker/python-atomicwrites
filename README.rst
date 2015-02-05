===================
python-atomicwrites
===================

.. image:: https://travis-ci.org/untitaker/python-atomicwrites.svg?branch=master
    :target: https://travis-ci.org/untitaker/python-atomicwrites

.. image:: https://ci.appveyor.com/api/projects/status/vadc4le3c27to59x/branch/master?svg=true
   :target: https://ci.appveyor.com/project/untitaker/python-atomicwrites/branch/master


Atomic file writes.

Features that distinguish it from other similar libraries:

- Race-free assertion that the target file doesn't yet exist. This can be
  controlled with the ``overwrite`` parameter.

- Windows support, although untested. The MSDN resources are not very explicit
  about which operations are atomic. This requires ``pywin32``.

- Simple high-level API that wraps a very flexible class-based API.

Usage::

    from atomicwrites import atomic_write

    with atomic_write('foo.txt') as f:
        f.write('Hello world.')
        # "foo.txt" doesn't exist yet.

    # Now it does.

License
=======

Licensed under the MIT, see ``LICENSE``.
