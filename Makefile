install:
	poetry install

run:
	poetry run gendiff -h

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 gendiff
	poetry run flake8 test

tests:
	poetry run pytest

by:
	poetry build
	python3 -m pip install --force-reinstall dist/*.whl
	poetry run flake8 gendiff
	poetry run flake8 test
	poetry run pytest
