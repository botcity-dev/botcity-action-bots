_install_dev:
	pip install -r test-requirements.txt
	pre-commit install --allow-missing-config

_install_prod:
	pip install -r requirements.txt

_flake8:
	@flake8 --show-source src/

_isort-fix:
	@isort src/

_isort:
	@isort --diff --check-only src/

_test:
	@pytest -v -vrxs

_coverage:
	@pytest --cov=src/ --cov-report term-missing

_mypy:
	@mypy --namespace-packages -p src

_docstring:
	@flake8 --show-source src/ --docstring-convention google

lint: _flake8 _isort _mypy _docstring
format-code: _isort-fix ## Format code
dev: _install_prod _install_dev
prod: _install_prod
test: _test
coverage: _coverage
mypy: _mypy