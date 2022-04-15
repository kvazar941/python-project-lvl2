install:
	poetry install

run:
	poetry run gendiff -h

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

lint:
	poetry run flake8 gendiff

tests:
	poetry run pytest
