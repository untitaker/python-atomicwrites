from atomicwrites import atomic_write, FileExistsError

import pytest


def test_atomic_write(tmpdir):
    fname = tmpdir.join('ha')
    for i in range(2):
        with atomic_write(str(fname), overwrite=True) as f:
            f.write('hoho')

    with pytest.raises(FileExistsError):
        with atomic_write(str(fname), overwrite=False) as f:
            f.write('haha')

    assert fname.read() == 'hoho'
    assert len(tmpdir.listdir()) == 1


def test_teardown(tmpdir):
    fname = tmpdir.join('ha')
    with pytest.raises(AssertionError):
        with atomic_write(str(fname), overwrite=True) as f:
            assert False

    assert not tmpdir.listdir()


def test_replace_simultaneously_created_file(tmpdir):
    fname = tmpdir.join('ha')
    with atomic_write(str(fname), overwrite=True) as f:
        f.write('hoho')
        fname.write('harhar')
        assert fname.read() == 'harhar'
    assert fname.read() == 'hoho'
    assert len(tmpdir.listdir()) == 1


def test_dont_remove_simultaneously_created_file(tmpdir):
    fname = tmpdir.join('ha')
    with pytest.raises(FileExistsError):
        with atomic_write(str(fname), overwrite=False) as f:
            f.write('hoho')
            fname.write('harhar')
            assert fname.read() == 'harhar'
    assert fname.read() == 'harhar'
    assert len(tmpdir.listdir()) == 1
