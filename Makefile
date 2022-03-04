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
	poetry run test './tests/fixtures/flat/file1.json' './tests/fixtures/flat/file2.json'
	poetry run test './tests/fixtures/flat/file3.yml' './tests/fixtures/flat/file4.yaml'

