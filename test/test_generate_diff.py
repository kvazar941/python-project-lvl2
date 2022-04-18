from gendiff.scripts.gendiff import generate_diff

TEST_DATA = [{'file_one': 'file1.json',
            'file_two': 'file2.json',
            'stylish': 'result_stylish.txt',
            'plain': 'result_plain.txt',
            'json': 'result_json.txt',
            'dir': './test/fixtures/flat/'
            },
            {'file_one': 'file3.yml',
            'file_two': 'file4.yaml',
            'stylish': 'result_stylish.txt',
            'plain': 'result_plain.txt',
            'json': 'result_json.txt',
            'dir': './test/fixtures/flat/'
            },
            {'file_one': 'file1.json',
            'file_two': 'file2.json',
            'stylish': 'result_stylish.txt',
            'plain': 'result_plain.txt',
            'json': 'result_json.txt',
            'dir': './test/fixtures/recursive/'
            },
            {'file_one': 'file3.yml',
            'file_two': 'file4.yaml',
            'stylish': 'result_stylish.txt',
            'plain': 'result_plain.txt',
            'json': 'result_json.txt',
            'dir': './test/fixtures/recursive/'
            }
        ]


def file_read(way):
    file_ = open(way)
    result = file_.read()[:-1]
    file_.close()
    return result


def test_generate_diff():
    for x in TEST_DATA:
        coll = [x['dir'] + x['file_one'], x['dir'] + x['file_two']]
        for y in ['stylish', 'plain', 'json']:
            test = generate_diff(*coll, y)
            result = file_read(x['dir'] + x[y])
            assert type(test) == str
            assert result == test
