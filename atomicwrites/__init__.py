import contextlib
import os
import sys
import tempfile

__version__ = '0.1.2'

if sys.platform != 'win32':
    def replace_atomic(src, dst):
        os.rename(src, dst)

    def move_atomic(src, dst):
        os.link(src, dst)
        os.unlink(src)
else:
    import win32api
    import win32con

    _windows_default_flags = win32con.WRITE_THROUGH

    def replace_atomic(src, dst):
        win32api.MoveFileEx(
            src, dst,
            win32con.MOVEFILE_REPLACE_EXISTING | _windows_default_flags
        )

    def move_atomic(src, dst):
        win32api.MoveFileEx(
            src, dst,
            _windows_default_flags
        )


replace_atomic.__doc__ = \
    '''
    Move ``src`` to ``dst``. If ``dst`` exists, it will be silently
    overwritten.

    Both paths must reside on the same filesystem for the operation to be
    atomic.
    ''' + (replace_atomic.__doc__ or '')


move_atomic.__doc__ = \
    '''
    Move ``src`` to ``dst``. There might a timewindow where both filesystem
    entries exist. If ``dst`` already exists, an error will be raised.

    Both paths must reside on the same filesystem for the operation to be
    atomic.
    ''' + (move_atomic.__doc__ or '')


class AtomicWriter(object):
    '''
    A helper class for performing atomic writes. Usage::

        with AtomicWriter(path).open() as f:
            f.write(...)


    It uses a temporary file in the same directory as the given path. This
    ensures that the temporary file resides on the same filesystem.

    The temporary file will then be atomically moved to the target location: On
    POSIX, it will use ``rename`` if files should be overwritten, otherwise a
    combination of ``link`` and ``unlink``. On Windows, it uses ``MoveFileEx``
    (see MSDN_) with the appropriate flags.

    .. _MSDN::
        https://msdn.microsoft.com/en-us/library/windows/desktop/aa365240%28v=vs.85%29.aspx

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
        except:
            self.rollback()
            raise
        else:
            self.commit()

    def get_fileobject(self, mode):
        '''Return the temporary path to use.'''
        tmpdir = os.path.dirname(self._path)
        f = tempfile.NamedTemporaryFile(mode=mode, dir=tmpdir, delete=False)
        self._tmppath = f.name
        return f

    def commit(self):
        '''Move the temporary file to the target location.'''
        if self._overwrite:
            os.rename(self._tmppath, self._path)  # atomic
        else:
            os.link(self._tmppath, self._path)  # atomic, fails if file exists
            os.unlink(self._tmppath)

    def rollback(self):
        '''Clean up all temporary resources.'''
        os.unlink(self._tmppath)


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
