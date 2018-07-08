import os
from .result_archiver import ResultArchiver


class TravisCI(ResultArchiver):
    @property
    def as_ci(self):
        return "TRAVIS_CI" in os.environ

    def _get_build_number(self):
        return os.environ.get("TRAVIS_BUILD_NUMBER")

    def _get_branch_name(self):
        os.environ.get("TRAVIS_BRANCH")
