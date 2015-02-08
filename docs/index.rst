.. include:: ../README.rst

.. module:: atomicwrites

API
===

.. autofunction:: atomic_write


Errorhandling
-------------

All filesystem errors are subclasses of :py:exc:`OSError`.

- On UNIX systems, errors from the Python stdlib calls are simply uncaught.
- On Windows systems, some PyWin32 errors are intercepted such that they
  resemble the stdlib exceptions. The original PyWin32 exception object is
  available as ``windows_error`` at all times.

.. exception:: FileExistsError

    This is Python 3's builtin ``FileExistsError``, under Python 2 it's a
    subclass of ``OSError`` with similar semantics.

.. exception:: FileNotFoundError

    This is Python 3's builtin ``FileNotFoundError``, under Python 2 it's a
    subclass of ``OSError`` with similar semantics.

Low-level API
-------------

.. autofunction:: replace_atomic

.. autofunction:: move_atomic

.. autoclass:: AtomicWriter
   :members:

License
-------

.. include:: ../LICENSE
