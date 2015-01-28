===================
python-atomicwrites
===================

.. image:: https://travis-ci.org/untitaker/python-atomicwrites.svg?branch=master
    :target: https://travis-ci.org/untitaker/python-atomicwrites

Atomic file writes on POSIX.

Usage::

    from atomicwrites import atomic_write

    with atomic_write('foo.txt') as f:
        f.write('Hello world.')
        # "foo.txt" doesn't exist yet.

    # Now it does.

License
=======

Licensed under the MIT, see ``LICENSE``.
