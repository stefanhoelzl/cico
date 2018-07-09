from pathlib import Path
from unittest import mock

from cico.results import File, Directory, Badge
from cico.results.results import Result, Copy


class TestResult:
    def test_return_from_to(self, dest):
        returns = [Path("file"), Path("dir")]
        with mock.patch.object(Result, "_to", return_value=returns):
            assert returns == Result().to(dest)

    def test_ensure_dest(self, tmpdir):
        dest = Path(str(tmpdir)) / "dest"
        with mock.patch.object(Result, "_to", return_value=[]):
            Result().to(dest)
        assert dest.is_dir()


class TestCopy:
    def test_copy_item(self, dest):
        with mock.patch.object(Copy, "_copy_item") as copy_item_mock:
            Copy("file0").to(dest)
        copy_item_mock.assert_has_calls([
            mock.call(Path("file0"), dest, "file0"),
        ])

    def test_rename(self, dest):
        with mock.patch.object(Copy, "_copy_item"):
            copied = Copy("src/file0",
                          destination="dest", rename="renamed").to(dest)
            assert [dest / "dest/renamed"] == copied

    def test_return_correct_path(self, dest):
        with mock.patch.object(Copy, "_copy_item"):
            assert [dest / "dest/file0"] \
                   == Copy("src/file0", destination="dest").to(dest)


class TestFile:
    def test_single_file(self, tmpdir, dest):
        tmpdir.join("file").ensure()
        File("file").to(dest)
        assert (dest / "file").is_file()

    def test_with_destination(self, tmpdir, dest):
        tmpdir.join("file").ensure()
        File("file", destination="sub").to(dest)
        assert (dest / "sub/file").is_file()

    def test_rename(self, tmpdir, dest):
        tmpdir.join("file").ensure()
        File("file", destination="sub", rename="renamed").to(dest)
        assert (dest / "sub/renamed").is_file()


class TestDirecotry:
    def test_single_directory_with_file(self, tmpdir, dest):
        tmpdir.join("dir").join("file").ensure()
        Directory("dir").to(dest)
        assert (dest / "dir").is_dir()
        assert (dest / "dir" / "file").is_file()

    def test_to_destination(self, tmpdir, dest):
        tmpdir.join("dir").join("file").ensure()
        Directory("dir", destination="sub").to(dest)
        assert (dest / "sub" / "dir").is_dir()
        assert (dest / "sub" / "dir" / "file").is_file()

    def test_rename(self, tmpdir, dest):
        tmpdir.join("dir").join("file").ensure()
        Directory("dir", destination="sub", rename="renamed").to(dest)
        assert (dest / "sub" / "renamed").is_dir()
        assert (dest / "sub" / "renamed" / "file").is_file()


class TestBadge:
    def test_create_svg(self, dest):
        Badge("badge", label="MyBadge", value="0").to(dest)
        assert (dest / "badge.svg").is_file()

    def test_create_png(self, dest):
        Badge("badge", label="MyBadge", value="0", png=True).to(dest)
        assert (dest / "badge.png").is_file()
