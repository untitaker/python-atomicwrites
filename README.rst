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

Usage:

.. code-block:: python

    from atomicwrites import atomic_write

    with atomic_write('foo.txt') as f:
        f.write('Hello world.')
        # "foo.txt" doesn't exist yet.

    # Now it does.

How it works
============

It uses a temporary file in the same directory as the given path. This ensures
that the temporary file resides on the same filesystem.

The temporary file will then be atomically moved to the target location: On
POSIX, it will use ``rename`` if files should be overwritten, otherwise a
combination of ``link`` and ``unlink``. On Windows, it uses ``MoveFileEx`` (see
MSDN_) with the appropriate flags.

Note that with ``link`` and ``unlink``, there's a timewindow where the file
might be available under two entries in the filesystem: The name of the
temporary file, and the name of the target file.

.. _MSDN: https://msdn.microsoft.com/en-us/library/windows/desktop/aa365240%28v=vs.85%29.aspx


License
=======

Licensed under the MIT, see ``LICENSE``.
