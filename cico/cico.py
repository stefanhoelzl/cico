import os
from pathlib import Path
from contextlib import contextmanager
from tempfile import TemporaryDirectory

from git import Repo


AS_CI = "CI" in os.environ


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
        self.repo = repo
        self.result_branch = branch
        self.results = results
        self.git_repo = None
        self.repo_dir = None
        self.destination = None

    def get_build_number(self):
        raise NotImplementedError()

    def get_branch_name(self):
        raise NotImplementedError()

    @property
    def branch_name(self):
        return self.get_branch_name() if AS_CI else "NO-CI"

    def commit(self, message=None, no_ci_push=False):
        if not message:
            message = "build #{build} on branch '{branch}'"
        with self._commit_to_repo(message, no_ci_push):
            self.add_results_files_to_index()

    def add_results_files_to_index(self):
        for result in self.results:
            added_files = result.to(self.destination)
            self.git_repo.index.add([str(f.relative_to(self.repo_dir))
                                     for f in added_files])

    @contextmanager
    def _commit_to_repo(self, message, no_ci_push):
        with TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            self.repo_dir = temp_dir
            self.destination = temp_dir / self.branch_name
            self.git_repo = Repo.clone_from(str(self.repo), temp_dir,
                                            branch=self.result_branch)
            if self.destination.is_dir():
                self.git_repo.index.remove([str(self.destination)],
                                           working_tree=True)
            self.destination.mkdir(exist_ok=True)
            yield
            self.git_repo.index.commit(message.format(
                branch=self.branch_name,
                build=self.get_build_number() if AS_CI else "NO-CI",
            ))
            if AS_CI or no_ci_push:
                self.git_repo.remote("origin").push()


class TravisCI(ResultArchiver):
    def get_build_number(self):
        return os.environ.get("TRAVIS_BUILD_NUMBER")

    def get_branch_name(self):
        os.environ.get("TRAVIS_BRANCH")
