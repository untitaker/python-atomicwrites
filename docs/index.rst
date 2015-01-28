.. include:: ../README.rst

API
===

.. autofunction:: atomicwrites.atomic_write

Low-level API
-------------

.. autoclass:: atomicwrites.AtomicWriterBase
   :members: open

.. autoclass:: atomicwrites.PosixAtomicWriter
   :members: open

.. class:: atomicwrites.AtomicWriter

   Automatically selected writer for the current OS.
