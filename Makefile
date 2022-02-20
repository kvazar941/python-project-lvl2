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
