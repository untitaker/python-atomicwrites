from atomicwrites import atomic_write

import pytest


def test_atomic_write(tmpdir):
    fname = tmpdir.join('ha')
    for i in range(2):
        with atomic_write(str(fname), overwrite=True) as f:
            f.write('hoho')

    with pytest.raises(OSError):
        with atomic_write(str(fname), overwrite=False) as f:
            f.write('haha')

    assert fname.read() == 'hoho'


def test_teardown(tmpdir):
    fname = tmpdir.join('ha')
    with pytest.raises(AssertionError):
        with atomic_write(str(fname), overwrite=True) as f:
            assert False

    assert not tmpdir.listdir()
