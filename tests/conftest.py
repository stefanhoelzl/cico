import os
from pathlib import Path

import pytest


@pytest.fixture
def dest(tmpdir):
    return Path(str(tmpdir.mkdir("dest")))


@pytest.fixture
def tmpdir(tmpdir):
    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    yield tmpdir
    os.chdir(cwd)
