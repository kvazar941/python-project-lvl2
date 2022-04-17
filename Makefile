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

tests:
	poetry run pytest

by:
	poetry build
	python3 -m pip install --force-reinstall dist/*.whl
	poetry run flake8 gendiff
	poetry run pytest
	poetry run gendiff -h
	poetry run gendiff -f stylish ./test/fixtures/recursive/file1.json ./test/fixtures/recursive/file4.yaml
