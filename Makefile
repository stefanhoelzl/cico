.PHONY: default
default: all;

.PHONY: tests
tests:
	PYTHONPATH=. pytest tests

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
