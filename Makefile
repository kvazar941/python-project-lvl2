install:
	poetry install

run:
	poetry run gendiff

build:
	poetry build
	python3 -m pip install --force-reinstall dist/*.whl

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 gendiff

test:
	poetry run test './tests/fixtures/file1.json' './tests/fixtures/file2.json'
	poetry run test './tests/fixtures/file3.yml' './tests/fixtures/file4.yaml'

