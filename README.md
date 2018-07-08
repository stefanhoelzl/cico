# cico
cico stores results created during a CI in a special git branch

cico.py
```python
from cico import TravisCI
from cico.results import Directory, File, Badge

TravisCI(
    repo = GitHub(USERNAME, REPO_NAME, TOKEN),
    branch = "ci-results",
    no_ci_commit = True,
    results = [
        Files("testresults.tap", "covhtml"),
        Badge(),
    ]
).commit()
```

.travis.yml
```yaml
after_script:
  - python cico.py

```
