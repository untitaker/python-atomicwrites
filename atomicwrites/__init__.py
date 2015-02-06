import contextlib
import errno
import os
import sys
import tempfile

__version__ = '0.1.3'


PY2 = sys.version_info[0] == 2

if PY2:
    class FileExistsError(OSError):
        errno = errno.EEXIST
else:
    # For some reason we have to redefine this, or users can't import it.
    FileExistsError = FileExistsError


if sys.platform != 'win32':
    @contextlib.contextmanager
    def handle_errors():
        try:
            yield
        except FileExistsError:
            raise
        except OSError as e:
            if e.errno == errno.EEXIST:
                raise FileExistsError(str(e))
            else:
                raise

    def _replace_atomic(src, dst):
        os.rename(src, dst)

    def _move_atomic(src, dst):
        os.link(src, dst)
        os.unlink(src)
else:
    import win32api
    import win32file
    import pywintypes

    _windows_default_flags = win32file.MOVEFILE_WRITE_THROUGH

    @contextlib.contextmanager
    def handle_errors():
        try:
            yield
        except pywintypes.error as e:
            if e.winerror == 183:
                raise FileExistsError(str(e))
            else:
                raise

    def _replace_atomic(src, dst):
        win32api.MoveFileEx(
            src, dst,
            win32file.MOVEFILE_REPLACE_EXISTING | _windows_default_flags
        )

    def _move_atomic(src, dst):
        win32api.MoveFileEx(
            src, dst,
            _windows_default_flags
        )


def replace_atomic(src, dst):
    '''
    Move ``src`` to ``dst``. If ``dst`` exists, it will be silently
    overwritten.

    Both paths must reside on the same filesystem for the operation to be
    atomic.
    '''
    with handle_errors():
        return _replace_atomic(src, dst)


def move_atomic(src, dst):
    '''
    Move ``src`` to ``dst``. There might a timewindow where both filesystem
    entries exist. If ``dst`` already exists, :py:exc:`FileExistsError` will be
    raised.

    Both paths must reside on the same filesystem for the operation to be
    atomic.
    '''
    with handle_errors():
        return _move_atomic(src, dst)


class AtomicWriter(object):
    '''
    A helper class for performing atomic writes. Usage::

        with AtomicWriter(path).open() as f:
            f.write(...)

    :param path: The destination filepath. May or may not exist.
    :param overwrite: If set to false, an error is raised if ``path`` exists.
        Either way, the operation is atomic.
    '''

    def __init__(self, path, overwrite=False):
        self._path = path
        self._overwrite = overwrite

    def open(self, mode='w'):
        '''
        Open the temporary file.
        '''
        return self._open(lambda: self.get_fileobject(mode=mode))

    @contextlib.contextmanager
    def _open(self, get_fileobject):
        try:
            with get_fileobject() as f:
                yield f
            self.commit()
        except:
            try:
                self.rollback()
            except Exception:
                pass
            raise

    def get_fileobject(self, mode):
        '''Return the temporary path to use.'''
        tmpdir = os.path.dirname(self._path)
        f = tempfile.NamedTemporaryFile(mode=mode, dir=tmpdir, delete=False)
        self._tmppath = f.name
        return f

    def commit(self):
        '''Move the temporary file to the target location.'''
        if self._overwrite:
            replace_atomic(self._tmppath, self._path)  # atomic
        else:
            move_atomic(self._tmppath, self._path)

    def rollback(self):
        '''Clean up all temporary resources.'''
        os.unlink(self._tmppath)


def atomic_write(path, mode='w', overwrite=False, writer_cls=AtomicWriter,
                 **open_kwargs):
    '''
    Simple atomic writes. This wraps :py:class:`AtomicWriter`::

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
