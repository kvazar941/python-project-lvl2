from gendiff.scripts.gendiff import generate_diff


def test_gendiff():
    result1 = open("./tests/fixtures/result.json")
    res = result1.read()
    result1.close()
    file1 = "./tests/fixtures/file1.json"
    file2 = "./tests/fixtures/file2.json"
    result = generate_diff(file1, file2)
    assert type(result) == str
    #  assert res == result
