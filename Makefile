install:
	poetry install

run:
	poetry run gendiff -h

build:
	poetry build
	python3 -m pip install --force-reinstall dist/*.whl
	poetry run pytest
publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 gendiff

tests:
	poetry run pytest
