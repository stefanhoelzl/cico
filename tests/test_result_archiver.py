from pathlib import Path
from unittest import mock

from cico.result_archiver import ResultArchiver
from cico.results.results import Result


class ResultMock(Result):
    def __init__(self, *files):
        self.files = files

    def _to(self, dest):
        return self.files


def create_result_archiver(repo=None, branch="branch", results=()):
    repo = repo if repo else mock.MagicMock()
    return ResultArchiver(repo, branch, results)


@mock.patch("cico.result_archiver.GitRepo")
@mock.patch("cico.result_archiver.TemporaryDirectory.__enter__")
def test_commit_ci(td_mock, repo_mock, monkeypatch, tmpdir):
    td_mock.return_value = tmpdir
    monkeypatch.setenv("CI", "CI")
    ResultArchiver._get_build_number = mock.MagicMock(return_value="99")
    ResultArchiver._get_branch_name = mock.MagicMock(return_value="feature")
    ResultArchiver("URL", "results", [
        ResultMock(Path("file0")),
        ResultMock(Path("file1"), Path("file2")),
    ]).commit()
    repo_mock.assert_has_calls([
        mock.call("URL"),
        mock.call().clone(Path(tmpdir), branch="results"),
        mock.call().rmdir(Path(tmpdir / "feature")),
        mock.call().add((Path("file0"),)),
        mock.call().add((Path("file1"), Path("file2"))),
        mock.call().commit("build #99 on branch 'feature'"),
        mock.call().push()
    ])
    assert (Path(tmpdir) / "feature").is_dir()


@mock.patch("cico.result_archiver.GitRepo")
@mock.patch("cico.result_archiver.TemporaryDirectory.__enter__")
def test_commit_ci_custom_message(td_mock, repo_mock, monkeypatch, tmpdir):
    td_mock.return_value = tmpdir
    monkeypatch.setenv("CI", "CI")
    ResultArchiver._get_build_number = mock.MagicMock(return_value="99")
    ResultArchiver._get_branch_name = mock.MagicMock(return_value="feature")
    ResultArchiver("URL", "results", [
        ResultMock(Path("file0")),
        ResultMock(Path("file1"), Path("file2")),
    ]).commit("{branch} {build}")
    repo_mock.assert_has_calls([
        mock.call("URL"),
        mock.call().clone(Path(tmpdir), branch="results"),
        mock.call().rmdir(Path(tmpdir / "feature")),
        mock.call().add((Path("file0"),)),
        mock.call().add((Path("file1"), Path("file2"))),
        mock.call().commit("feature 99"),
        mock.call().push()
    ])
    assert (Path(tmpdir) / "feature").is_dir()


@mock.patch("cico.result_archiver.GitRepo")
@mock.patch("cico.result_archiver.TemporaryDirectory.__enter__")
def test_commit_no_ci(td_mock, repo_mock, monkeypatch, tmpdir):
    td_mock.return_value = tmpdir
    monkeypatch.delenv("CI",raising=False)
    url_mock = mock.MagicMock()
    ResultArchiver(url_mock, "results", [
        ResultMock(Path("file0"))
    ]).commit()
    url_mock.set_authentication.assert_called_once_with(system=True)
    repo_mock.assert_has_calls([
        mock.call(url_mock),
        mock.call().clone(Path(tmpdir), branch="results"),
        mock.call().rmdir(Path(tmpdir / "NO_CI")),
        mock.call().add((Path("file0"),)),
        mock.call().commit("build #NO_CI on branch 'NO_CI'"),
    ])
    assert (Path(tmpdir) / "NO_CI").is_dir()



@mock.patch("cico.result_archiver.GitRepo")
@mock.patch("cico.result_archiver.TemporaryDirectory.__enter__")
def test_commit_no_ci_push_anyways(td_mock, repo_mock, monkeypatch, tmpdir):
    td_mock.return_value = tmpdir
    monkeypatch.delenv("CI",raising=False)
    url_mock = mock.MagicMock()
    ResultArchiver(url_mock, "results", [
        ResultMock(Path("file0"))
    ]).commit(no_ci_push=True)
    url_mock.set_authentication.assert_called_once_with(system=True)
    repo_mock.assert_has_calls([
        mock.call(url_mock),
        mock.call().clone(Path(tmpdir), branch="results"),
        mock.call().rmdir(Path(tmpdir / "NO_CI")),
        mock.call().add((Path("file0"),)),
        mock.call().commit("build #NO_CI on branch 'NO_CI'"),
        mock.call().push()
    ])
    assert (Path(tmpdir) / "NO_CI").is_dir()


@mock.patch("cico.result_archiver.GitRepo")
@mock.patch("cico.result_archiver.TemporaryDirectory.__enter__")
def test_commit_result(td_mock, repo_mock, monkeypatch, tmpdir):
    td_mock.return_value = tmpdir
    monkeypatch.setenv("CI", "CI")
    ResultArchiver._get_build_number = mock.MagicMock(return_value="99")
    ResultArchiver._get_branch_name = mock.MagicMock(return_value="feature")
    commit_result = ResultArchiver("URL", "results", [
        ResultMock(Path("file0")),
        ResultMock(Path("file1"), Path("file2")),
    ]).commit()
    assert "feature" == commit_result["branch"]
