.PHONY: default
default: all;

.PHONY: tests
tests: tests.unit tests.roundtrip

.PHONY: tests.unit
tests.unit:
	PYTHONPATH=. pytest tests

.PHONY: tests.roundtrip
tests.roundtrip:
	PYTHONPATH=. python tests/roundtrip.py

.PHONY: release.build
release.build:
	python setup.py sdist bdist_wheel

.PHONY: release.upload
release.upload: release.build
	twine upload ${OPTS} dist/*

.PHONY: env.install
env.install:
	python -m pip install -r requirements.txt

.PHONY: all
all: tests release.build

.PHONY: ci
ci: all
