# cico
cico stores results created during a CI in a special git branch

cico.py
```python
from cico import TravisCI
from cico.results import Directory, File, Badge

TravisCI(
    repo = GitHub(USERNAME, REPO_NAME, TOKEN),
    branch = "ci-results",
    no_ci_push = True,  # performs a push even if not run in a CI environment
    results = [
        Files("testresults.tap", destination="tap"),
        Directory("covhtml", destination="coverage"),
        Badge("badges/mybadge", png=True, label="My Badge", value=96,
              **anybadge_arguments),  # https://github.com/jongracecox/anybadge
    ]
).commit()
```

.travis.yml
```yaml
after_script:
  - python cico.py
```
