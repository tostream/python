def convertArrVertoHor(arr):
    result = []
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if len(result) < j + 1:
                intarr = []
            else:
                intarr = result.pop(j)
            intarr.append(arr[i][j])
            result.insert(j, intarr)
    return result


def shiftrow(arr, shuffkey, maskkey):
    from random import randint
    result = []
    for i in arr[0]:
        int_arr = [i]

        for j in range(1, len(arr)):
            if j in shuffkey:
                int_arr.append(randomreplacechar(arr[j].pop(randint(0, len(arr[j]) - 1))))
            elif j in maskkey:
                int_arr.append(maskidenitfyid(arr[j].pop(randint(0, len(arr[j]) - 1))))
            else:
                int_arr.append(arr[j].pop(randint(0, len(arr[j]) - 1)))
        result.append(int_arr)
    return result


def randomreplacechar(charvalue):
    import random
    if charvalue == "" or charvalue.strip() == "":
        return charvalue
    inds = [i for i, _ in enumerate(charvalue) if not charvalue.isspace()]
    samplesize = min(3, len(inds))
    sam = random.sample(inds, samplesize)
    from string import ascii_letters

    lst = list(charvalue)
    for ind in sam:
        lst[ind] = random.choice(ascii_letters)

    return "".join(lst)


def maskidenitfyid(idvalue):
    if len(idvalue) < 4:
        return 'xxxx'
    else:
        return idvalue[:len(idvalue) - 4] + 'xxxx'


def readcsv(path):
    import csv
    with open(path, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        your_list = list(reader)
    return your_list


def writecsv(path, array):
    import csv
    with open(path, 'w', newline="", encoding="utf-8") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, lineterminator='\r\n')
        for line in array:
            wr.writerow(line)


for i in range(19):
    pre_load_array = readcsv("C:\\tmp\\vti_address_csv\\0000" + str(i).zfill(2) + "_0")
    # header = pre_load_array.pop(0)
    working_array = convertArrVertoHor(pre_load_array)
    resultarray = shiftrow(working_array, [], [])  # customer log #
    # resultarray = shiftrow(working_array, [10, 11], [18, 19, 28])
    # resultarray = shiftrow(working_array, [10, 11], [18, 19, 28])
    # exportarray = resultarray.insert(0, header)
    writecsv("C:\\tmp\\vti_customer_addr" + str(i) + ".csv", resultarray)
