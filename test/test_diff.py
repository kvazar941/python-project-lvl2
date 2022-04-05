from gendiff.scripts.gendiff import generate_diff


def test_gendiff():
    file1 = "./test/fixtures/flat/file1.json"
    file2 = "./test/fixtures/flat/file2.json"
    file_ = open("./test/fixtures/flat/result.txt")
    result = file_.read()
    file_.close()
    format_='stylish'
    a = generate_diff(file1, file2, format_)
    assert type(a) == str
    assert result == a
