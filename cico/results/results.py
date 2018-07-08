import shutil
from distutils.dir_util import copy_tree
from pathlib import Path


class Result:
    _dest = Path(".")

    def to(self, dest):
        dest = dest / self._dest
        dest.mkdir(exist_ok=True)
        return self._to(dest)

    def _to(self, dest):
        raise NotImplementedError()


class Copy(Result):
    def __init__(self, *items, destination=""):
        self._items = [Path(item) for item in items]
        self._dest = destination

    def _copy_item(self, item, dest):
        raise NotImplementedError()

    def _to(self, dest):
        copied = []
        for item in self._items:
            self._copy_item(item, dest)
            copied.append(dest / item.name)
        return copied


class File(Copy):
    def _copy_item(self, item, dest):
        shutil.copy2(item, dest)


class Directory(Copy):
    def _copy_item(self, item, dest):
        dest = dest / item.name
        copy_tree(str(item), str(dest))
