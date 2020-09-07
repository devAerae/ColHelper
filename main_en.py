import os
import gzip
import zlib
import base64
import xmltodict


def read_file(path: str) -> str:
    fr = open(path, 'rb')
    data = fr.read()
    fr.close()
    return data.decode('utf-8')


def xor(string: str, key: int) -> str:
    return ''.join(chr(ord(char) ^ key) for char in string)


def decrypt_data(data: str) -> str:
    base64_decoded = base64.urlsafe_b64decode(xor(data, key=11).encode())
    decompressed = gzip.decompress(base64_decoded)
    return decompressed.decode()


def encrypt_data(data: str) -> str:
    gzipped = gzip.compress(data.encode())
    base64_encoded = base64.urlsafe_b64encode(gzipped)
    return xor(base64_encoded.decode(), key=11)


def decode_level(level_data: str) -> str:
    base64_decoded = base64.urlsafe_b64decode(level_data.encode())
    decompressed = zlib.decompress(base64_decoded, 15 | 32)
    return decompressed.decode()


def encode_level(level_string: str) -> str:
    gzipped = gzip.compress(level_string.encode())
    base64_encoded = base64.urlsafe_b64encode(gzipped)
    return base64_encoded.decode()


def process(map_string):
    col_string = str(decode_level(map_string)).split(';')[0].split(',')[1].split('|')
    del col_string[-1]

    obj_list = str(decode_level(map_string)).split(';')[1:]
    del obj_list[-1]

    col_array = []
    for i in range(len(col_string)):
        col_array = col_array + [col_string[i].split('_')]
    col_final = []
    for n in range(len(col_array)):
        temp = col_array[n]
        col_dict = {}
        for i in range(0, len(temp), 2):
            even = str(temp[i])
            odd = temp[i + 1]
            col_dict[even] = odd
        col_final = col_final + [col_dict]

    n1 = int(input('Please set the starting range :'))
    n2 = int(input('Please set the end range :'))

    obj_base = '1,899,2,1,3,15,36,1,'
    obj_fin = []
    for i in range(len(col_final)):
        if n1 - 1 < int(col_final[i]['6']) <= n2:
            obj_col = obj_base + '7,%s,8,%s,9,%s,' % (col_final[i]['1'], col_final[i]['2'], col_final[i]['3'])
            obj_time = obj_col + '10,0,'
            obj_opa = obj_time + '35,%s' % (col_final[i]['7'])
            if '5' in col_final[i]:
                obj_opa = obj_opa + ',17,%s' % (col_final[i]['5'])
            if '17' in col_final[i]:
                obj_opa = obj_opa + ',60,%s' % (col_final[i]['17'])
            obj_ch = obj_opa + ',23,%s' % (col_final[i]['6'])
            if '9' in col_final[i]:
                obj_ch = obj_ch + ',50,%s' % (col_final[i]['9'])
            if '10' in col_final[i]:
                obj_ch = obj_ch + ',49,%s' % (col_final[i]['10'])
            obj_final = obj_ch
            obj_fin = obj_fin + [obj_final]

    obj_string = ';'.join(obj_fin) + ';'
    changed_map = 'H4sIAAAAAAAAA' + encode_level(decode_level(map_string) + obj_string)[13:]
    print('Adding Col trigger(s)...')

    fr = open(fPath + 'CCLocalLevels.dat', 'wb')
    fr.write(encrypt_data(fin.replace(map_string, changed_map)).encode())
    fr.close()
    print('Completed successfully!')


def print_txt():
    for a in range(len(levels)):
        b = 0
        if ',' in levels[a]['s'][b] or levels[a]['s'][b].isdigit() and len(levels[a]['s'][b]) < 4:
            b += 1
        print(levels[a]['s'][b])
    number = int(input('Select level by number :')) - 1
    if number < 0 or number > len(levels) - 1:
        print('Incorrect input!')
    else:
        lvl = 1
        while 'H4sIAAAAAAAA' not in levels[number]['s'][lvl]:
            lvl += 1
        else:
            process(levels[number]['s'][lvl])


def restore():
    fr = open(fPath + 'CCLocalLevels.dat', 'wb')
    fr.write(res.encode())
    fr.close()
    print('Restored successfully!')


fPath = os.getenv('localappdata') + '\\GeometryDash\\'

res = read_file(fPath + 'CCLocalLevels.dat')
fin = decrypt_data(res)
dic = xmltodict.parse(fin)
levels = dic['plist']['dict']['d']['d']

txt = '''
1. Select level
2. Restore 'CCLocalLevels.dat'
3. exit
'''
num = 0
while num != 3:
    num = int(input(txt))
    if num == 1:
        print_txt()
    if num == 2:
        restore()
    if num == 3:
        break
