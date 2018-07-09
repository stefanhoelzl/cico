import os
import time
import ssl
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory

from cico import TravisCI, File, GitHub


with TemporaryDirectory() as temp:
    current_time = str(time.time())
    temp_file = Path(temp) / "roundtrip"
    temp_file.write_text(current_time)

    commit_result = TravisCI(
        repo=GitHub("stefanhoelzl", "ci-results",
                    os.environ.get("GITHUB_TOKEN", "")),
        branch="cico-testing",
        results=[
            File(temp_file)
        ]
    ).commit(no_ci_push=True)

ssl._create_default_https_context = ssl._create_unverified_context
REPO_URL = "https://raw.githubusercontent.com/stefanhoelzl/ci-results"
URL = "{}/cico-testing/{}/roundtrip".format(REPO_URL, commit_result["branch"])

retrieved_time = ""
while current_time != retrieved_time \
        and float(current_time)+5*60 > time.time():
    urllib.request.urlcleanup()
    retrieved_time = urllib.request.urlopen(URL).read().decode("utf-8").strip()
    time.sleep(1)
assert current_time == retrieved_time
