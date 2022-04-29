"""test module."""
import pytest

from gendiff.differ import generate_diff
from gendiff.read_file import get_content

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


TEST_DATA = [
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


@pytest.mark.parametrize('file_a,file_b,formatter,expected', TEST_DATA)
def test_generate_diff(file_a, file_b, formatter, expected):
    """
    Testing generate_diff.

    Args:
        file_a: str
        file_b: str
        formatter: str
        expected: str

    """
    assert isinstance(generate_diff(file_a, file_b, formatter), str)
    content_file = get_content(expected)
    assert content_file[:-1] == generate_diff(file_a, file_b, formatter)
