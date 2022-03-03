from gendiff.scripts.gendiff import generate_diff


def test_gendiff():
    result = open("./tests/fixtures/result.txt")
    res = result.read()
    result.close()
    file1 = "./tests/fixtures/file1.json"
    file2 = "./tests/fixtures/file2.json"
    file3 = "./tests/fixtures/file3.yml"
    file4 = "./tests/fixtures/file4.yaml"
    result1 = generate_diff(file1, file2) 
    assert type(generate_diff(file1, file2)) == str
    assert res == result1
    #assert res == generate_diff(file3, file4)
    #assert res == generate_diff(file1, file4)
    #assert res == generate_diff(file2, file3)
