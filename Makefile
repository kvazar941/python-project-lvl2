install:
	poetry install

run:
	poetry run gendiff -h

build:
	poetry build
	python3 -m pip install --force-reinstall dist/*.whl
	poetry run pytest
	poetry run gendiff -h
	gendiff -f stylish ./test/fixtures/flat/file1.json ./test/fixtures/flat/file2.json

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 gendiff

tests:
	poetry run pytest
