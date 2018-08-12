import pytest
from tempfile import TemporaryDirectory
import os
from os.path import join as pjoin

from atomicwrites import AtomicFolder, FolderAlreadyExists


def test_atomic_path_happy_path():
    with TemporaryDirectory() as base_path:
        dst = pjoin(base_path, "atomic")
        with AtomicFolder(dst) as path:
            print(path)
            assert not os.path.isdir(dst)
            assert os.path.isdir(path)

        assert os.path.isdir(dst)
        assert not os.path.isdir(path)


def test_raise_if_dst_already_exists():
    with TemporaryDirectory() as base_path:
        dst = pjoin(base_path, "atomic")
        os.makedirs(dst)  # assume the folder already exists

        with pytest.raises(FolderAlreadyExists):
            with AtomicFolder(dst) as path:
                pass

        # we didn't touch the exitsing folder
        assert os.path.isdir(dst)
        # and didn't create a tmp folder
        assert not os.path.isdir(AtomicFolder.to_tmp(dst))


def test_delete_tmp_on_failure():
    with TemporaryDirectory() as base_path:
        dst = pjoin(base_path, "atomic")

        with pytest.raises(ValueError):
            with AtomicFolder(dst, delete_on_failure=True) as path:
                # some operation goes wrong
                raise ValueError

        assert not os.path.isdir(dst)
        assert not os.path.isdir(AtomicFolder.to_tmp(dst))
