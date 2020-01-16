import os
import os.path
import math


def remap_keys(d):
    if not isinstance(d, dict):
        return d
    rslt = []
    for k, v in d.items():
        k = remap_keys(k)
        v = remap_keys(v)
        rslt.append({'products': k, 'count': v})
    return rslt


def file_exist(folder, filename):
    from os import path
    full_path = os.path.join(file_path, folder, filename)
    return path.exists(full_path)


def get_file_list(folder):
    from os import walk
    filename_arr = []
    full_path = os.path.join(file_path, folder)
    for (dirpath, dirnames, filenames) in walk(full_path):
        for i in sorted(filenames):
            filename_arr.append(i)
    return filename_arr


def write_csv(full_path, array, multi_line=False, mode='w+'):
    import csv
    with open(full_path, mode, newline="", encoding="utf-8") as my_file:
        wr = csv.writer(my_file, quoting=csv.QUOTE_ALL, lineterminator='\r\n')
        if multi_line:
            for line in array:
                wr.writerow(line)
        else:
            wr.writerow(array)


def read_csv(file_path):
    import csv
    with open(file_path, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        your_list = list(reader)
    return your_list


def read_gz_csv(file_path):
    import gzip
    import csv
    with gzip.open(file_path, 'rt') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    return your_list


def read_gz_data_file(folder, filename):
    full_path = os.path.join(file_path, folder, filename)
    return read_gz_csv(full_path)


def read_data_file(folder, filename):
    full_path = os.path.join(file_path, folder, filename)
    return read_csv(full_path)


def write_result(folder, filename, result, multi_line=False):
    full_path = os.path.join(file_path, folder, filename)
    write_csv(full_path, result, multi_line)


def save_json(full_path, content, mode='w'):
    import json
    with open(full_path, mode) as json_file:
        json.dump(content, json_file)


def export_json(folder, filename, content, mode='w'):
    full_path = os.path.join(file_path, folder, filename)
    save_json(full_path, content, mode)


def export_result():
    # folder = "result"
    # json_export = []
    # filenames = get_file_list(folder)
    # for filename in filenames:
    #    json_export.append(read_data_file('result', filename))
    # export_json('json', 'result.json', json_export, 'w+')
    export_json('json', 'result.json', remap_keys(temp_result_arr), 'w+')


def split_data():
    input_file = read_gz_data_file('', source_file_name)
    count = len(input_file)
    folder = 'split'
    split_arr = []
    filename = 1
    actual_count = 0
    for i in range(count):
        # clean the blank lines
        if len(input_file[i]) > 0:
            actual_count += 1
            split_arr.append(input_file[i])
        if actual_count == scale:
            write_result(folder, str(filename), split_arr, multi_line=True)
            filename += 1
            split_arr = []
            actual_count = 0
    # handle the set which len is smaller than scale
    if len(split_arr) > 0:
        write_result(folder, str(filename), split_arr, multi_line=True)


def combin_count(prod_1, prod_2):
    # folder = "result"
    # filename = "%s_%s" % (prod_1, prod_2)
    # combin_counter = [prod_1, prod_2, 0]

    # if file_exist(folder, filename):
    #    combin_counter = read_data_file(folder, filename)[0]
    # combin_counter[2] = int(combin_counter[2]) + 1
    # write_result(folder, filename, combin_counter)

    # 2020-01-16 new try
    if tuple([prod_1, prod_2]) in temp_result_arr:
        temp_result_arr[prod_1, prod_2] += 1
    else:
        temp_result_arr[prod_1, prod_2] = 1


def basket_check(basket_arr):
    while len(basket_arr) > 1:
        work_prod = basket_arr.pop(0)
        for j in basket_arr:
            combin_count(str(work_prod), str(j))


def product_combin_count():
    current_basket = ''
    current_basket_arr = []
    folder = "split"
    filenames = get_file_list(folder)
    for filename in filenames:
        data = read_data_file(folder, filename)
        for i in data:
            if len(i) > 0:
                if current_basket != i[0]:
                    basket_check(current_basket_arr)
                    current_basket_arr = []
                current_basket = i[0]
                current_basket_arr.append(i[1])
    # handle the last basket
    basket_check(current_basket_arr)


if __name__ == '__main__':
    import sys

    file_path = "C:\\Users\\ITDFWP\\Documents\\so1\\sample\\"
    source_file_name = "data_10.csv.gz"
    scale = 10000

    temp_result_arr = {}
    # if len(sys.argv) > 2:
    #    file_path = sys.argv[1]
    #    source_file_name = sys.argv[2]
    #    if len(sys.argv) > 3:
    #        scale = int(sys.argv[3])
    # else:
    #    print("'file path' 'source file name' 'scale',first 2 parameters are required, default scale is 10000")
    #    exit(1)
    from datetime import datetime

    dateTimeObj = datetime.now()
    print(dateTimeObj)
    split_data()
    dateTimeObj = datetime.now()
    print(dateTimeObj)
    product_combin_count()
    dateTimeObj = datetime.now()
    print(dateTimeObj)
    export_result()
    dateTimeObj = datetime.now()
    print(dateTimeObj)
