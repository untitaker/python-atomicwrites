import contextlib
import errno
import os
import sys
import tempfile

__version__ = '0.1.4'


PY2 = sys.version_info[0] == 2

text_type = unicode if PY2 else str


class _FileExistsError(OSError if PY2 else FileExistsError):
    errno = errno.EEXIST

class _FileNotFoundError(OSError if PY2 else FileNotFoundError):
    errno = errno.ENOENT

def _path_to_unicode(x):
    if not isinstance(x, text_type):
        return x.decode(sys.getfilesystemencoding())
    return x


if sys.platform != 'win32':
    @contextlib.contextmanager
    def handle_errors():
        yield

    def _replace_atomic(src, dst):
        os.rename(src, dst)

    def _move_atomic(src, dst):
        os.link(src, dst)
        os.unlink(src)
else:
    from ctypes import windll

    _MOVEFILE_REPLACE_EXISTING = 0x1
    _MOVEFILE_WRITE_THROUGH = 0x8

    _windows_default_flags = _MOVEFILE_WRITE_THROUGH
    _windows_error_table = {
        183: _FileExistsError,
        3: _FileNotFoundError
    }

    @contextlib.contextmanager
    def handle_errors():
        try:
            yield
        except pywintypes.error as e:
            native_cls = _windows_error_table.get(e.winerror, OSError)
            new_e = native_cls(e)
            new_e.windows_error = e
            raise new_e

    def _replace_atomic(src, dst):
        windll.kernel32.MoveFileExW(
            _path_to_unicode(src), _path_to_unicode(dst),
            _windows_default_flags | _MOVEFILE_REPLACE_EXISTING
        )

    def _move_atomic(src, dst):
        windll.kernel32.MoveFileExW(
            _path_to_unicode(src), _path_to_unicode(dst),
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
    :param mode: The filemode for the temporary file.
    :param overwrite: If set to false, an error is raised if ``path`` exists.
        Errors are only raised after the file has been written to.  Either way,
        the operation is atomic.

    If you need further control over the exact behavior, you are encouraged to
    subclass.
    '''

    def __init__(self, path, mode='w', overwrite=False):
        if 'a' in mode:
            raise ValueError(
                'Appending to an existing file is not supported, because that '
                'would involve an expensive `copy`-operation to a temporary '
                'file. Open the file in normal `w`-mode and copy explicitly '
                'if that\'s what you\'re after.'
            )
        if 'x' in mode:
            raise ValueError('Use the `overwrite`-parameter instead.')
        if 'w' not in mode:
            raise ValueError('AtomicWriters can only be written to.')

        self._path = path
        self._mode = mode
        self._overwrite = overwrite

    def open(self):
        '''
        Open the temporary file.
        '''
        return self._open(self.get_fileobject)

    @contextlib.contextmanager
    def _open(self, get_fileobject):
        try:
            with get_fileobject() as f:
                yield f
            self.commit(f)
        except:
            try:
                self.rollback(f)
            except Exception:
                pass
            raise

    def get_fileobject(self, dir=None, **kwargs):
        '''Return the temporary path to use.'''
        if dir is None:
            dir = os.path.dirname(self._path)
        return tempfile.NamedTemporaryFile(mode=self._mode, dir=dir,
                                           delete=False, **kwargs)

    def commit(self, f):
        '''Move the temporary file to the target location.'''
        if self._overwrite:
            replace_atomic(f.name, self._path)  # atomic
        else:
            move_atomic(f.name, self._path)

    def rollback(self, f):
        '''Clean up all temporary resources.'''
        os.unlink(f.name)


def atomic_write(path, writer_cls=AtomicWriter, **cls_kwargs):
    '''
    Simple atomic writes. This wraps :py:class:`AtomicWriter`::

        with atomic_write(path) as f:
            f.write(...)

    :param path: The target path to write to.

    Additional keyword arguments are passed to the writer class. See
    :py:class:`AtomicWriterBase`.
    '''
    return writer_cls(path, **cls_kwargs).open()
