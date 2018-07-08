import os
from pathlib import Path
from contextlib import contextmanager
from tempfile import TemporaryDirectory

from git import Repo


AS_CI = "CI" in os.environ


class GitRepo:
    def __init__(self, url):
        self.url = url
        self.repo = None
        self.base = None
        self.branch = None

    def clone(self, dest, branch):
        self.base = dest
        self.branch = branch
        self.repo = Repo.clone_from(str(self.url), dest, branch=branch)

    def rmdir(self, dir_):
        if dir_.is_dir():
            self.repo.index.remove([str(dir_)], working_tree=True)

    def add(self, files):
        self.repo.index.add([str(f.relative_to(self.base))
                             for f in files])

    def commit(self, message):
        self.repo.index.commit(message)

    def push(self):
        self.repo.remote("origin").push()


class GitHub:
    def __init__(self, user, repo, token):
        self.name = repo
        self.user = user
        self.token = token

    def __str__(self):
        authentication = "" if not AS_CI \
            else "{}:x-oauth-basic@".format(self.token)
        return "https://{}github.com/{}/{}.git".format(authentication,
                                                       self.user, self.name)


class ResultArchiver:
    def __init__(self, repo, branch, results):
        self.repo = GitRepo(repo)
        self.result_branch = branch
        self.results = results
        self.destination = None

    def _get_build_number(self):
        raise NotImplementedError()

    def _get_branch_name(self):
        raise NotImplementedError()

    @property
    def _branch_name(self):
        return self._get_branch_name() if AS_CI else "NO-CI"

    def commit(self, message=None, no_ci_push=False):
        if not message:
            message = "build #{build} on branch '{branch}'"
        with self._commit_to_repo(message, no_ci_push):
            self._add_results_files_to_index()

    def _add_results_files_to_index(self):
        for result in self.results:
            added_files = result.to(self.destination)
            self.repo.add(added_files)

    @contextmanager
    def _commit_to_repo(self, message, no_ci_push):
        with TemporaryDirectory() as repo_dir:
            self._prepare_repo(Path(repo_dir))
            yield
            self._finish_repo(message, no_ci_push)

    def _prepare_repo(self, dir_):
        self.destination = dir_ / self._branch_name
        self.repo.clone(dir_, branch=self.result_branch)
        self.repo.rmdir(self.destination)
        self.destination.mkdir(exist_ok=True)

    def _finish_repo(self, message, no_ci_push):
        self.repo.commit(message.format(
            branch=self._branch_name,
            build=self._get_build_number() if AS_CI else "NO-CI",
        ))
        if AS_CI or no_ci_push:
            self.repo.push()


class TravisCI(ResultArchiver):
    def _get_build_number(self):
        return os.environ.get("TRAVIS_BUILD_NUMBER")

    def _get_branch_name(self):
        os.environ.get("TRAVIS_BRANCH")
