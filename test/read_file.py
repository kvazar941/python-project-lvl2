from gendiff.scripts.gendiff import generate_diff


#def test(file1, file2, way_result, format_='stylish'):
#    file_ = open(way_result)
#    result = file_.read()
#    file_.close()
#    a = generate_diff(file1, file2, format_)
#    assert type(a) == str
#    if result != a:
#        print('wait:\n', result, len(result))
#        print('is:\n', a, len(a))
#    assert result == a
        

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
