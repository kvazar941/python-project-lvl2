from gendiff.scripts.gendiff import generate_diff


def test_gendiff():
    result = open("./tests/fixtures/flat/result.txt")
    res = result.read()
    result.close()
    result2 = open("./tests/fixtures/recursive/result.txt")
    res2 = result2.read()
    result2.close()
    file1 = "./tests/fixtures/flat/file1.json"
    file2 = "./tests/fixtures/flat/file2.json"
    file3 = "./tests/fixtures/flat/file3.yml"
    file4 = "./tests/fixtures/flat/file4.yaml"
    file5 = "./tests/fixtures/recursive/file1.json"
    file6 = "./tests/fixtures/recursive/file2.json"
    
    result1 = generate_diff(file1, file2) 
    assert type(generate_diff(file1, file2)) == str
    assert res == result1
    result1 = generate_diff(file3, file4)
    assert res == result1
    result3 = generate_diff(file5, file6)
    assert res2 == result3
