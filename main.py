from asyncio import windows_utils
from copyreg import constructor
import os
import gzip
from tkinter import messagebox
from turtle import width
import zlib
import base64
import xmltodict
from tkinter import *

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

def getn1():
    global n1Input, n1Popup
    n1Popup = Toplevel(listPopup)
    n1LabelText = StringVar()
    n1LabelText.set("시작 범위")
    n1Label = Label(n1Popup, textvariable=n1LabelText, height=4)
    n1Label.pack(side="left")
    n1Input = Entry(n1Popup, width=10)
    n1Input.pack(side="left")
    n1OkBtn = Button(n1Popup, width=5, text="확인", overrelief="solid", command=getn2)
    n1OkBtn.pack(side="left")

def getn2():
    global n2Input, n2Popup
    n2Popup = Toplevel(n1Popup)
    n2LabelText = StringVar()
    n2LabelText.set("끝 범위")
    n2Label = Label(n2Popup, textvariable=n2LabelText, height=4)
    n2Label.pack(side="left")
    n2Input = Entry(n2Popup, width=10)
    n2Input.pack(side="left")
    n2OkBtn = Button(n2Popup, width=5, text="확인", overrelief="solid", command=process)
    n2OkBtn.pack(side="left")

def process():
    number = int(inputBox.get()) - 1

    n1 = int(n1Input.get())
    n2 = int(n2Input.get())

    if number < 0 or number > len(levels) - 1:
        messagebox.showinfo("오류", "올바르지 않은 번호입니다")
    else:
        lvl = 1
        while 'H4sIAAAAAAAA' not in levels[number]['s'][lvl]:
            lvl += 1
        else:
            map_string = levels[number]['s'][lvl]

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

    obj_base = '1,899,2,1,3,15,36,1,'  # Col 오브젝트 배치
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

    fr = open(fPath + 'CCLocalLevels.dat', 'wb')
    fr.write(encrypt_data(fin.replace(map_string, changed_map)).encode())
    fr.close()
    listPopup.destroy()
    n1Popup.destroy()
    n2Popup.destroy()
    messagebox.showinfo("완료", "완료되었습니다")


def print_txt():
    global inputBox, listPopup
    listPopup = Toplevel(root)
    titleLabel = Label(listPopup, text="맵을 번호로 선택해주세요")
    okBtn = Button(listPopup, width=10, text="확인", overrelief="solid", command=getn1)
    titleLabel.pack()
    inputBox = Entry(listPopup, width=10)
    for a in range(len(levels)):
        b = 0
        if ',' in levels[a]['s'][b] or levels[a]['s'][b].isdigit() and len(levels[a]['s'][b]) < 4:
            b += 1
        levelLabel = Label(listPopup, text=(str(a + 1)) + '. ' + levels[a]['s'][b])
        levelLabel.pack()
    inputBox.pack()
    okBtn.pack()


def restore():
    fr = open(fPath + 'CCLocalLevels.dat', 'wb')
    fr.write(res.encode())
    fr.close()
    messagebox.showinfo("복원완료", "복원되었습니다")

def loadGUI():
    root.title("ColHelper")
    root.geometry("300x200")
    title = Label(root, text="ColHelper (한글)")
    title.pack()

    selectLevelBtn = Button(root, width=20, text="맵 선택하기", overrelief="solid", command=print_txt)
    restoreBtn = Button(root, width=20, text="맵 복원하기", overrelief="solid", command=restore)
    exitBtn = Button(root, width=20, text="나가기", overrelief="solid", command=exit)
    selectLevelBtn.pack()
    restoreBtn.pack()
    exitBtn.pack()



root = Tk()
fPath = os.getenv('localappdata') + '\\GeometryDash\\'
res = read_file(fPath + 'CCLocalLevels.dat')
fin = decrypt_data(res)
dic = xmltodict.parse(fin)
levels = dic['plist']['dict']['d']['d']

if __name__ == "__main__":
    loadGUI()
    root.mainloop()
