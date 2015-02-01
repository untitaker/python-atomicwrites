import codecs
import contextlib
import os
import tempfile

__version__ = '0.1.1'


class AtomicWriterBase(object):
    '''
    A helper class for performing atomic writes. Not fully implemented, you
    should use a subclass of it instead. Usage::

        with MyWriter(path).open() as f:
            f.write(...)

    :param path: The destination filepath. May or may not exist.
    :param overwrite: If set to false, an error is raised if ``path`` exists.
        Either way, the operation is atomic.
    '''

    def __init__(self, path, overwrite=False):
        self._path = path
        self._overwrite = overwrite

    def open(self, mode='w'):
        '''Prepare the temporary file object and return it.'''
        raise NotImplementedError()

    def commit(self):
        '''Move the temporary file to the target location.'''
        raise NotImplementedError()

    def rollback(self):
        '''Clean up all temporary resources.'''
        raise NotImplementedError()

    @contextlib.contextmanager
    def _open(self, get_fileobject):
        try:
            with get_fileobject() as f:
                yield f
        except:
            self.rollback()
            raise
        else:
            self.commit()


class PosixAtomicWriter(AtomicWriterBase):
    '''
    An implementation of :py:class:`AtomicWriterBase` for POSIX-compliant
    filesystems. It uses temporary files in the same directory.
    '''

    def get_fileobject(self, mode):
        '''Return the temporary path to use.'''
        tmpdir = os.path.dirname(self._path)
        f = tempfile.NamedTemporaryFile(mode=mode, dir=tmpdir, delete=False)
        self._tmppath = f.name
        return f

    def open(self, mode='w', **open_kwargs):
        '''
        Open the temporary file. Any arguments will be passed on to the builtin
        ``open`` function.
        '''
        return self._open(lambda: self.get_fileobject(mode=mode))

    def commit(self):
        if self._overwrite:
            os.rename(self._tmppath, self._path)  # atomic
        else:
            os.link(self._tmppath, self._path)  # atomic, fails if file exists
            os.unlink(self._tmppath)

    def rollback(self):
        os.unlink(self._tmppath)

AtomicWriter = PosixAtomicWriter  # for current OS


def atomic_write(path, mode='w', overwrite=False, writer_cls=AtomicWriter,
                 **open_kwargs):
    '''
    Simple atomic writes. This wraps :py:class:`AtomicWriterBase` and its
    subclasses::

        with atomic_write(path) as f:
            f.write(...)

    :param path: The target path to write to.
    :param mode: The mode to open the file with.
    :param overwrite: Whether to overwrite the target file if it already
        exists. Errors are only raised after the file has been written to.
    :param writer_cls: A custom writer class to use.

    Additional keyword arguments are passed to the ``open``-method of the
    writer class. See :py:meth:`AtomicWriterBase.open`.
    '''
    return writer_cls(path, overwrite=overwrite).open(mode=mode, **open_kwargs)
