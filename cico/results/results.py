import shutil
from distutils.dir_util import copy_tree
from pathlib import Path


class Result:
    def to(self, dest):
        dest = dest
        dest.mkdir(exist_ok=True)
        return self._to(dest)

    def _to(self, dest):
        raise NotImplementedError()


class Copy(Result):
    def __init__(self, item, destination=""):
        self._item = Path(item)
        self._dest = destination

    def to(self, dest):
        return super().to(dest / self._dest)

    def _copy_item(self, item, dest):
        raise NotImplementedError()

    def _to(self, dest):
        self._copy_item(self._item, dest)
        return [dest / self._item.name]


class File(Copy):
    def _copy_item(self, item, dest):
        shutil.copy2(str(item), str(dest))


class Directory(Copy):
    def _copy_item(self, item, dest):
        copy_tree(str(item), str(dest / item.name))
