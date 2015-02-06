.. include:: ../README.rst

.. module:: atomicwrites

API
===

.. autofunction:: atomic_write

.. exception:: FileExistsError

   This is Python 3's builtin ``FileExistsError``, under Python 2 it's a
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
