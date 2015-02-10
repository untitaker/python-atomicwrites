.. include:: ../README.rst

.. module:: atomicwrites

API
===

.. autofunction:: atomic_write


Errorhandling
-------------

All filesystem errors are subclasses of :py:exc:`OSError`.

- On UNIX systems, errors from the Python stdlib calls are simply uncaught.
- On Windows systems, PyWin32 errors are wrapped such that they somewhat
  resemble the stdlib exceptions. The original PyWin32 exception object is
  available as ``windows_error`` at all times.

Low-level API
-------------

.. autofunction:: replace_atomic

.. autofunction:: move_atomic

.. autoclass:: AtomicWriter
   :members:

License
-------

.. include:: ../LICENSE
