# SPDX-License-Identifier: WTFPL
# Based on code from https://github.com/bachya/simplisafe-python/blob/dev/Makefile
black:
	poetry run black teslajsonpy
coverage:
	poetry run pytest -s --verbose --cov-report term-missing --cov-report xml --cov=teslajsonpy tests -Wi -Wd:::teslajsonpy
clean:
	rm -rf dist/ build/ .egg teslajsonpy.egg-info/
init:
	pip3 install --upgrade pip poetry
	poetry lock
	poetry install
lint: flake8 docstyle pylint
flake8:
	poetry run flake8 teslajsonpy
docstyle:
	poetry run pydocstyle teslajsonpy
pylint:
	poetry run pylint teslajsonpy
publish: 
	poetry publish
test:
	poetry run pytest -s --verbose tests -Wi -Wd:::teslajsonpy
typing:
	poetry run mypy --ignore-missing-imports teslajsonpy
docs: docstyle
	poetry export --dev --without-hashes -f requirements.txt --output docs/requirements.txt
	poetry run sphinx-build -b html docs docs/html