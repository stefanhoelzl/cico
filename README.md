# cico

[![Build Status](https://travis-ci.org/stefanhoelzl/cico.svg?branch=master)](https://travis-ci.org/stefanhoelzl/cico)
[![PyPI](https://img.shields.io/pypi/v/cico.svg)](https://pypi.org/project/cico/)
[![License](https://img.shields.io/pypi/l/cico.svg)](LICENSE)

deploy CI results to git

`deploy.py`
```python
from cico import TravisCI
from cico.results import Directory, File, Badge

TravisCI(
    repo = GitHub(USERNAME,   # GitHub Username (e.g. 'stefanhoelzl')
                  REPO_NAME,  # GitHub Repository (e.g. 'ci-results')
                  TOKEN),     # GitHub Personal access tokens ()
                              # ONLY ENCRYPTED (https://docs.travis-ci.com/user/environment-variables/#Defining-encrypted-variables-in-.travis.yml)
    branch = RESULT_BRANCH,   # Git Branch with the results (e.g. 'cico-testing')
    results = [
        # Deploy file 'testresults.tap' into folder 'tap' (destination is optional)
        File("testresults.tap", destination="tap"),
        # Deploy directory 'covhtml' into folder 'coverage' (desitnation is optional)
        Directory("covhtml", destination="coverage"),
        # Create a Badge with the label "My Badge" and value "96" as .svg and .png (png is optional)
        Badge("badges/mybadge", png=True, label="My Badge", value=96,
              **anybadge_arguments),  # https://github.com/jongracecox/anybadge
    ]
).commit(
    message="build {build} on branch {branch}",  # commit message (optional)
    # perform push if not executed in CI envirionment (default=False)
    no_ci_push=True
)
```

`.travis.yml` with `after_script`
```yaml
after_script:
  - python deploy.py
```

`.travis.yml` with `deploy`
```yaml
deploy:
  provider: script
  script: python deploy.py
```
