from gendiff.scripts.gendiff import generate_diff


def test(file1, file2, way_result, format_='stylish'):
    file_ = open(way_result)
    result = file_.read()
    file_.close()
    a = generate_diff(file1, file2, format_)
    assert type(a) == str
    assert result == a


def test_gendiff():
    way_flat = "./tests/fixtures/flat/"
    #test(way_flat + "file1.json", way_flat + "file2.json", way_flat + 'result.txt', 'stylish')

    #test(way_flat + "file3.yml", way_flat + "file4.yaml", way_flat + 'result.txt', 'stylish')

    #test(way_flat + "file1.json", way_flat + "file2.json", way_flat + 'result_plain.txt', 'plain')
    
    #test(way_flat + "file3.yml", way_flat + "file4.yaml", way_flat + 'result_plain.txt', 'plain')
    
    way_recursive = "./tests/fixtures/recursive/"
    test(way_recursive + "file1.json", way_recursive + "file2.json", way_recursive + 'result.txt', 'stylish')

    #test(way_recursive + "file1.json", way_recursive + "file2.json", way_recursive + 'result_plain.txt', 'plain')
    
    #test(way_recursive + "file1.json", way_recursive + "file2.json", way_recursive + 'result_to_json.txt', 'json')

    print("all test's complete")
