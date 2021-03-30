# SPDX-License-Identifier: WTFPL
# Based on code from https://github.com/bachya/simplisafe-python/blob/dev/Makefile
black:
	pipenv run black teslajsonpy
coverage:
	pipenv run pytest -s --verbose --cov-report term-missing --cov-report xml --cov=teslajsonpy tests -Wi -Wd:::teslajsonpy
clean:
	rm -rf dist/ build/ .egg teslajsonpy.egg-info/
sync_deps:
	pipenv-setup sync --pipfile
init:
	pip3 install --upgrade pip pipenv
	pipenv lock
	pipenv install --three --dev
lint: flake8 docstyle pylint
flake8:
	pipenv run flake8 teslajsonpy
docstyle:
	pipenv run pydocstyle teslajsonpy
pylint:
	pipenv run pylint teslajsonpy
publish: sync_deps
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg teslajsonpy.egg-info/
test:
	pipenv run pytest -s --verbose tests -Wi -Wd:::teslajsonpy
typing:
	pipenv run mypy --ignore-missing-imports teslajsonpy
docs: docstyle
	pipenv lock -r --dev > docs/requirements.txt
	echo "teslajsonpy" >> docs/requirements.txt
	pipenv run sphinx-build -b html docs docs/html