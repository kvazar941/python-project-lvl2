from gendiff.scripts.gendiff import generate_diff


dir_flat = './test/fixtures/flat/'
dir_recursive = './test/fixtures/recursive/'


test_result = ['result_stylish.txt', 'result_plain.txt', 'result_json.txt']


test_data = [('file1.json', "file2.json"),
            ('file3.yml', "file4.yaml"),
        ]


formats = ['stylish', 'plain', 'json']


def file_read(way):
    file_ = open("./test/fixtures/flat/result_stylish.txt")
    result = file_.read()
    file_.close()
    return result


def test_generate_diff():
    coll = ["./test/fixtures/flat/file1.json", "./test/fixtures/flat/file2.json", 'stylish']
    result = file_read("./test/fixtures/flat/result_stylish.txt")
    test = generate_diff(*coll)
    assert type(test) == str
    assert result == test
