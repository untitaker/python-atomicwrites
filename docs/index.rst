.. include:: ../README.rst

.. module:: atomicwrites

API
===

.. autofunction:: atomic_write

Low-level API
-------------

.. autoclass:: AtomicWriterBase
   :members: open

.. autoclass:: PosixAtomicWriter
   :members: open

.. class:: AtomicWriter

   Automatically selected writer for the current OS.

License
-------

.. include:: ../LICENSE
