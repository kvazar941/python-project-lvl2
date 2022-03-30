install:
	poetry install

run:
	poetry run gendiff

build:
	poetry build
	python3 -m pip install --force-reinstall dist/*.whl
	poetry run test 'first_file', 'second_file'

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest
