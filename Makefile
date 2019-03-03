coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=teslajsonpy tests
init:
	pip3 install pip pipenv
	pipenv --python 3
	pipenv lock
	pipenv install --three --dev
lint:
	pipenv run flake8 teslajsonpy
	pipenv run pydocstyle teslajsonpy
	pipenv run pylint teslajsonpy
publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg teslajsonpy.egg-info/
test:
	pipenv run py.test
typing:
	pipenv run mypy --ignore-missing-imports teslajsonpy
