===================
python-atomicwrites
===================

.. image:: https://travis-ci.org/untitaker/python-atomicwrites.svg?branch=master
    :target: https://travis-ci.org/untitaker/python-atomicwrites

.. image:: https://ci.appveyor.com/api/projects/status/vadc4le3c27to59x/branch/master?svg=true
   :target: https://ci.appveyor.com/project/untitaker/python-atomicwrites/branch/master

Atomic file writes.

.. code-block:: python

    from atomicwrites import atomic_write

    with atomic_write('foo.txt', overwrite=True) as f:
        f.write('Hello world.')
        # "foo.txt" doesn't exist yet.

    # Now it does.


Features that distinguish it from other similar libraries (see alternatives_).

- Race-free assertion that the target file doesn't yet exist. This can be
  controlled with the ``overwrite`` parameter.

- Windows support, although untested. The MSDN resources are not very explicit
  about which operations are atomic.

- Simple high-level API that wraps a very flexible class-based API.

- Consistent error handling across platforms.


How it works
============

It uses a temporary file in the same directory as the given path. This ensures
that the temporary file resides on the same filesystem.

The temporary file will then be atomically moved to the target location: On
POSIX, it will use ``rename`` if files should be overwritten, otherwise a
combination of ``link`` and ``unlink``. On Windows, it uses ``MoveFileEx`` (see
MSDN_) through stdlib's ``ctypes`` with the appropriate flags.

Note that with ``link`` and ``unlink``, there's a timewindow where the file
might be available under two entries in the filesystem: The name of the
temporary file, and the name of the target file.

.. _MSDN: https://msdn.microsoft.com/en-us/library/windows/desktop/aa365240%28v=vs.85%29.aspx

.. alternatives:

Alternatives
============

``python-atomicwrites`` is inspired by some of the following libraries,
however, no code has been directly taken from them:

- The Trac project's `utility functions
  <http://www.edgewall.org/docs/tags-trac-0.11.7/epydoc/trac.util-pysrc.html>`_,
  also used in `Werkzeug <http://werkzeug.pocoo.org/>`_ and
  `mitsuhiko/python-atomicfile
  <https://github.com/mitsuhiko/python-atomicfile>`_.

- `abarnert/fatomic <https://github.com/abarnert/fatomic>`_

- `sashka/atomicfile <https://github.com/sashka/atomicfile>`_

License
=======

Licensed under the MIT, see ``LICENSE``.
