"""test module."""
from gendiff.scripts.gendiff import generate_diff

FLAT_JSON_ONE = './test/fixtures/flat/file1.json'
FLAT_JSON_TWO = './test/fixtures/flat/file2.json'
FLAT_YML_ONE = './test/fixtures/flat/file3.yml'
FLAT_YML_TWO = './test/fixtures/flat/file4.yaml'
FLAT_STYLISH = './test/fixtures/flat/result_stylish.txt'
FLAT_PLAIN = './test/fixtures/flat/result_plain.txt'
FLAT_JSON = './test/fixtures/flat/result_json.txt'
RECURSIVE_JSON_ONE = './test/fixtures/recursive/file1.json'
RECURSIVE_JSON_TWO = './test/fixtures/recursive/file2.json'
RECURSIVE_YML_ONE = './test/fixtures/recursive/file3.yml'
RECURSIVE_YML_TWO = './test/fixtures/recursive/file4.yaml'
RECURSIVE_STYLISH = './test/fixtures/recursive/result_stylish.txt'
RECURSIVE_PLAIN = './test/fixtures/recursive/result_plain.txt'
RECURSIVE_JSON = './test/fixtures/recursive/result_json.txt'

STYLISH = 'stylish'
PLAIN = 'plain'
JSON = 'json'


TEST_DATA = [  # noqa WPS407
    (FLAT_JSON_ONE, FLAT_JSON_TWO, STYLISH, FLAT_STYLISH),
    (FLAT_YML_ONE, FLAT_YML_TWO, STYLISH, FLAT_STYLISH),
    (FLAT_JSON_ONE, FLAT_JSON_TWO, PLAIN, FLAT_PLAIN),
    (FLAT_YML_ONE, FLAT_YML_TWO, PLAIN, FLAT_PLAIN),
    (FLAT_JSON_ONE, FLAT_JSON_TWO, JSON, FLAT_JSON),
    (FLAT_YML_ONE, FLAT_YML_TWO, JSON, FLAT_JSON),
    (RECURSIVE_JSON_ONE, RECURSIVE_JSON_TWO, STYLISH, RECURSIVE_STYLISH),
    (RECURSIVE_YML_ONE, RECURSIVE_YML_TWO, STYLISH, RECURSIVE_STYLISH),
    (RECURSIVE_JSON_ONE, RECURSIVE_JSON_TWO, PLAIN, RECURSIVE_PLAIN),
    (RECURSIVE_YML_ONE, RECURSIVE_YML_TWO, PLAIN, RECURSIVE_PLAIN),
    (RECURSIVE_JSON_ONE, RECURSIVE_JSON_TWO, JSON, RECURSIVE_JSON),
    (RECURSIVE_YML_ONE, RECURSIVE_YML_TWO, JSON, RECURSIVE_JSON),
]


def file_read(way):
    with open(way) as file_name:
        return file_name.read()[:-1]


def test_generate_diff():
    for coll in TEST_DATA:
        file_a, file_b, formatter, diff = coll
        assert isinstance(generate_diff(file_a, file_b, formatter), str)
        assert file_read(diff) == generate_diff(file_a, file_b, formatter)
