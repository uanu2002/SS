from tkinter import *
from tkinter import filedialog
import tkinter.messagebox  # 弹窗库
from PIL import Image, ImageDraw, ImageFont, ImageTk
import matplotlib.pyplot as plt
import cv2
import shutil
import numpy as np
import random
import os
from utils import *
import hashlib
quant = np.array([[16, 11, 10, 16, 24, 40, 51, 61],  # QUANTIZATION TABLE
                  [12, 12, 14, 19, 26, 58, 60, 55],  # required for DCT
                  [14, 13, 16, 24, 40, 57, 69, 56],
                  [14, 17, 22, 29, 51, 87, 80, 62],
                  [18, 22, 37, 56, 68, 109, 103, 77],
                  [24, 35, 55, 64, 81, 104, 113, 92],
                  [49, 64, 78, 87, 103, 121, 120, 101],
                  [72, 92, 95, 98, 112, 100, 103, 99]])

global choosepic_LSB_basic
global LSB_text_len
global DCT_text_len
DCT_text_len = 10
global LSB_suijijiange_step
LSB_suijijiange_step = 2
global LSB_suijijiange_text_len
global LSB_quyujiaoyan_size
LSB_quyujiaoyan_size = 4
global LSB_quyujiaoyan_text_len


# str1为载体图片路径，str2为隐写文件，str3为加密图片保存的路径
def func_LSB_yinxie(str1, str2, str3):
    im = Image.open(str1)
    # 获取图片的宽和高
    global width, height
    width = im.size[0]
    print("width:" + str(width) + "\n")
    height = im.size[1]
    print("height:" + str(height) + "\n")
    count = 0
    # 获取需要隐藏的信息
    key = get_key(str2)
    print('key: ', key)
    keylen = len(key)
    print('keylen: ', keylen)

    for h in range(0, height):
        for w in range(0, width):
            pixel = im.getpixel((w, h))
            # code.interact(local=locals())
            a = pixel[0]
            b = pixel[1]
            c = pixel[2]
            if count == keylen:
                break
            # 下面的操作是将信息隐藏进去
            # 分别将每个像素点的RGB值余2，这样可以去掉最低位的值
            # 再从需要隐藏的信息中取出一位，转换为整型
            # 两值相加，就把信息隐藏起来了
            a = a - mod(a, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            b = b - mod(b, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            c = c - mod(c, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            if count % 3 == 0:
                im.putpixel((w, h), (a, b, c))
    im.save(str3)
    tkinter.messagebox.showinfo('提示', '图像隐写已完成,隐写后的图像保存为' + str3)


# le为所要提取的信息的长度，str1为加密载体图片的路径，str2为提取文件的保存路径
def func_LSB_tiqu(le, str1, str2):
    a = ""
    b = ""
    im = Image.open(str1)
    # lenth = le*8
    lenth = le
    width = im.size[0]
    height = im.size[1]
    count = 0
    for h in range(0, height):
        for w in range(0, width):
            # 获得(w,h)点像素的值
            pixel = im.getpixel((w, h))
            # 此处余3，依次从R、G、B三个颜色通道获得最低位的隐藏信息
            if count % 3 == 0:
                count += 1
                b = b + str((mod(int(pixel[0]), 2)))
                if count == lenth:
                    break
            if count % 3 == 1:
                count += 1
                b = b + str((mod(int(pixel[1]), 2)))
                if count == lenth:
                    break
            if count % 3 == 2:
                count += 1
                b = b + str((mod(int(pixel[2]), 2)))
                if count == lenth:
                    break
        if count == lenth:
            break

    print(b)

    with open(str2, "wb") as f:
        for i in range(0, len(b), 8):
            # 以每8位为一组二进制，转换为十进制
            stra = toasc(b[i:i + 8])
            # stra = b[i:i+8]
            # 将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
            stra = chr(stra)
            sb = bytes(stra, encoding="utf8")
            # print(sb)
            # f.write(chr(stra))
            f.write(sb)
            stra = ""
    f.closed


def LSB_yinxie():
    tkinter.messagebox.showinfo('提示', '请选择要进行LSB隐写的图像')
    Fpath = filedialog.askopenfilename()
    shutil.copy(Fpath, './')

    old = Fpath.split('/')[-1]

    global choosepic_LSB_basic
    choosepic_LSB_basic = old

    # 处理后输出的图片路径
    new = old[:-4] + "_LSB-generated." + old[-3:]

    # 需要隐藏的信息
    tkinter.messagebox.showinfo('提示', '请选择要隐藏的信息(请选择txt文件)')
    txtpath = filedialog.askopenfilename()
    shutil.copy(txtpath, './')
    enc = txtpath.split('/')[-1]
    # #print(enc)
    # plt.imshow(old)
    # plt.show()
    func_LSB_yinxie(old, enc, new)

    global LSB_new
    LSB_new = new

    old = cv2.imread(old)
    new = cv2.imread(new)

    plt.figure(figsize=(6, 7))  # matplotlib设置画面大小 600*700
    # plt.suptitle('LSB信息隐藏')
    b, g, r = cv2.split(old)
    old = cv2.merge([r, g, b])
    b, g, r = cv2.split(new)
    new = cv2.merge([r, g, b])

    plt.subplot(2, 2, 1)
    plt.imshow(old)
    plt.title("原始图像")
    plt.subplot(2, 2, 2)
    plt.hist(old.ravel(), 256, [0, 256])
    plt.title("原始图像直方图")
    plt.subplot(2, 2, 3)
    plt.imshow(new)
    plt.title("隐藏信息的图像")
    plt.subplot(2, 2, 4)
    plt.hist(new.ravel(), 256, [0, 256])
    plt.title("隐藏信息图像直方图")
    plt.tight_layout()  # 设置默认的间距
    plt.show()


def LSB_tiqu():
    # le = text_len
    global LSB_text_len
    le = int(LSB_text_len)
    print('le: ', le)

    tkinter.messagebox.showinfo('提示', '请选择要进行LSB提取的图像')
    Fpath = filedialog.askopenfilename()

    LSB_new = Fpath
    tkinter.messagebox.showinfo('提示', '请选择将提取信息保存的位置')
    tiqu = filedialog.askdirectory()
    # print(tiqu)

    tiqu = tiqu + '/LSB_recover.txt'
    func_LSB_tiqu(le, LSB_new, tiqu)
    tkinter.messagebox.showinfo('提示', '隐藏信息已提取,请查看LSB_recover.txt')


def DCT_yinxie():
    tkinter.messagebox.showinfo('提示', '请选择要进行DCT隐写的图像')
    Fpath = filedialog.askopenfilename()
    shutil.copy(Fpath, './')

    original_image_file = Fpath.split('/')[-1]
    # original_image_file是DCT_origin.bmp
    y = cv2.imread(original_image_file, 0)

    row, col = y.shape
    row = int(row / 8)
    col = int(col / 8)

    y1 = y.astype(np.float32)
    Y = cv2.dct(y1)

    tkinter.messagebox.showinfo('提示', '请选择要隐藏的信息(请选择txt文件)')
    txtpath = filedialog.askopenfilename()
    shutil.copy(txtpath, './')
    tmp = txtpath.split('/')[-1]
    # tmp是hideInfo_DCT.txt

    msg = get_key(tmp)

    count = len(msg)
    print('count: ', count)
    k1, k2 = randinterval(row, col, count, 12)

    for i in range(0, count):
        k1[i] = (k1[i] - 1) * 8 + 1
        k2[i] = (k2[i] - 1) * 8 + 1

    # 信息嵌入
    temp = 0
    H = 1
    for i in range(0, count):
        if msg[i] == '0':
            if Y[k1[i] + 4, k2[i] + 1] > Y[k1[i] + 3, k2[i] + 2]:
                Y[k1[i] + 4, k2[i] + 1], Y[k1[i] + 3, k2[i] + 2] = swap(Y[k1[i] + 4, k2[i] + 1],
                                                                        Y[k1[i] + 3, k2[i] + 2])
        else:
            if Y[k1[i] + 4, k2[i] + 1] < Y[k1[i] + 3, k2[i] + 2]:
                Y[k1[i] + 4, k2[i] + 1], Y[k1[i] + 3, k2[i] + 2] = swap(Y[k1[i] + 4, k2[i] + 1],
                                                                        Y[k1[i] + 3, k2[i] + 2])

        if Y[k1[i] + 4, k2[i] + 1] > Y[k1[i] + 3, k2[i] + 2]:
            Y[k1[i] + 3, k2[i] + 2] = Y[k1[i] + 3, k2[i] + 2] - H  # 将小系数调整更小
        else:
            Y[k1[i] + 4, k2[i] + 1] = Y[k1[i] + 4, k2[i] + 1] - H

    y2 = cv2.idct(Y)

    global dct_encoded_image_file
    dct_encoded_image_file = original_image_file[:-4] + "_DCT-generated." + original_image_file[-3:]

    cv2.imwrite(dct_encoded_image_file, y2)

    old = cv2.imread(original_image_file)
    new = cv2.imread(dct_encoded_image_file)

    tkinter.messagebox.showinfo('提示', '图像隐写已完成,隐写后的图像保存为' + dct_encoded_image_file)

    b, g, r = cv2.split(old)
    old = cv2.merge([r, g, b])
    b, g, r = cv2.split(new)
    new = cv2.merge([r, g, b])

    plt.figure(figsize=(6, 7))  # matplotlib设置画面大小 600*700

    plt.subplot(2, 2, 1)
    plt.imshow(old)
    plt.title("原始图像")
    plt.subplot(2, 2, 2)
    plt.hist(old.ravel(), 256, [0, 256])
    plt.title("原始图像直方图")
    plt.subplot(2, 2, 3)
    plt.imshow(new)
    plt.title("隐藏信息的图像")
    plt.subplot(2, 2, 4)
    plt.hist(new.ravel(), 256, [0, 256])
    plt.title("隐藏信息图像直方图")
    plt.tight_layout()  # 设置默认的间距
    plt.show()


def DCT_tiqu():
    count = int(DCT_text_len)
    print('count: ', count)

    tkinter.messagebox.showinfo('提示', '请选择要进行DCT提取的图像')
    Fpath = filedialog.askopenfilename()
    dct_encoded_image_file = Fpath.split('/')[-1]
    # dct_encoded_image_file = './LS'
    dct_img = cv2.imread(dct_encoded_image_file, 0)
    print(dct_img)
    y = dct_img
    y1 = y.astype(np.float32)
    Y = cv2.dct(y1)
    row, col = y.shape
    row = int(row / 8)
    col = int(col / 8)
    # count = 448
    k1, k2 = randinterval(row, col, count, 12)
    for i in range(0, count):
        k1[i] = (k1[i] - 1) * 8 + 1
        k2[i] = (k2[i] - 1) * 8 + 1

    # 准备提取并回写信息
    str2 = 'DCT_recover.txt'
    b = ""

    for i in range(0, count):
        if Y[k1[i] + 4, k2[i] + 1] < Y[k1[i] + 3, k2[i] + 2]:
            b = b + str('0')
        # print('msg[i]: ',0)
        else:
            b = b + str('1')
        # print('msg[i]: ',1)

    print(b)

    tkinter.messagebox.showinfo('提示', '请选择将提取信息保存的位置')
    tiqu = filedialog.askdirectory()
    tiqu = tiqu + '/DCT_hidden_text.txt'

    str2 = tiqu
    with open(str2, "wb") as f:
        for i in range(0, len(b), 8):
            # 以每8位为一组二进制，转换为十进制
            stra = toasc(b[i:i + 8])
            # stra = b[i:i+8]
            # 将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
            stra = chr(stra)
            sb = bytes(stra, encoding="utf8")
            f.write(sb)
            stra = ""
    f.closed

    tkinter.messagebox.showinfo('提示', '隐藏信息已提取,请查看DCT_hidden_text.txt')


# 图像降级改进
def Image1_yinxie():
    tkinter.messagebox.showinfo('提示', '请选择载体图像')
    Fpath = filedialog.askopenfilename()

    shutil.copy(Fpath, './')

    beiyinxie_image = Fpath.split('/')[-1]

    tkinter.messagebox.showinfo('提示', '请选择要隐写的图像')
    Fpath = filedialog.askopenfilename()
    shutil.copy(Fpath, './')
    mark_image = Fpath.split('/')[-1]

    img = np.array(Image.open(beiyinxie_image))
    mark = np.array(Image.open(mark_image))
    rows, cols, dims = mark.shape

    for i in range(0, dims):
        for j in range(0, rows * 2):
            for k in range(0, cols * 2):
                img[j, k, i] = img[j, k, i] & 252

    for i in range(0, dims):
        for j in range(0, rows):
            for k in range(0, cols):
                img[2 * j, 2 * k, i] = img[2 * j, 2 * k, i] + (mark[j, k, i] & 192) // 64
                img[2 * j, 2 * k + 1, i] = img[2 * j, 2 * k + 1, i] + (mark[j, k, i] & 48) // 16
                img[2 * j + 1, 2 * k, i] = img[2 * j + 1, 2 * k, i] + (mark[j, k, i] & 12) // 4
                img[2 * j + 1, 2 * k + 1, i] = img[2 * j + 1, 2 * k + 1, i] + (mark[j, k, i] & 3)
            # print(2*j+1,2*k+1)
    img = Image.fromarray(img)
    global new_image
    new_image = beiyinxie_image[:-4] + "_with_mark1." + beiyinxie_image[-3:]

    img.save(new_image)

    tkinter.messagebox.showinfo('提示', '图像隐写已完成,隐写后的图像保存为' + new_image)

    old = cv2.imread(beiyinxie_image)
    new = cv2.imread(new_image)

    b, g, r = cv2.split(old)
    old = cv2.merge([r, g, b])
    b, g, r = cv2.split(new)
    new = cv2.merge([r, g, b])

    plt.figure(figsize=(6, 7))  # matplotlib设置画面大小 600*700
    # plt.suptitle('LSB信息隐藏')
    plt.subplot(2, 2, 1)
    plt.imshow(old)
    plt.title("原始图像")
    plt.subplot(2, 2, 2)
    plt.hist(old.ravel(), 256, [0, 256])
    plt.title("原始图像直方图")
    plt.subplot(2, 2, 3)
    plt.imshow(new)
    plt.title("隐藏信息的图像")
    plt.subplot(2, 2, 4)
    plt.hist(new.ravel(), 256, [0, 256])
    plt.title("隐藏信息图像直方图")
    plt.tight_layout()  # 设置默认的间距
    plt.show()


# 图像降级改进
def Image1_tiqu():
    tkinter.messagebox.showinfo('提示', '请选择要进行提取图片水印的图像')
    Fpath = filedialog.askopenfilename()
    new_image = Fpath

    tkinter.messagebox.showinfo('提示', '请选择将提取信息保存的位置')
    tiqu = filedialog.askdirectory()

    print(tiqu)
    tiqu = tiqu + '/mark_get1.' + new_image[-3:]
    print(tiqu)

    imgwmark = np.array(Image.open(new_image))
    result = imgwmark
    rows, cols, dims = imgwmark.shape
    rows = rows // 2
    cols = cols // 2
    for i in range(0, dims):
        for j in range(0, rows * 2):
            for k in range(0, cols * 2):
                imgwmark[j, k, i] = imgwmark[j, k, i] & 3

    for i in range(0, dims):
        for j in range(0, rows):
            for k in range(0, cols):
                result[j, k, i] = imgwmark[2 * j, 2 * k, i] * 64 + imgwmark[2 * j, 2 * k + 1, i] * 16
                +imgwmark[2 * j + 1, 2 * k, i] * 4 + imgwmark[2 * j + 1, 2 * k + 1, i]
    mark_get = Image.fromarray(result)
    mark_get.save(tiqu)

    tkinter.messagebox.showinfo('提示', '水印图片已提取,请查看mark_get1.' + new_image[-3:])


# 图像降级
def Image_yinxie():
    tkinter.messagebox.showinfo('提示', '请选择载体图像')
    Fpath = filedialog.askopenfilename()

    shutil.copy(Fpath, './')

    beiyinxie_image = Fpath.split('/')[-1]

    tkinter.messagebox.showinfo('提示', '请选择要隐写的图像')
    Fpath = filedialog.askopenfilename()
    shutil.copy(Fpath, './')
    mark_image = Fpath.split('/')[-1]

    img = np.array(Image.open(beiyinxie_image))
    mark = np.array(Image.open(mark_image))
    rows, cols, dims = mark.shape

    for i in range(0, dims):
        for j in range(0, rows * 2):
            for k in range(0, cols * 2):
                img[j, k, i] = img[j, k, i] & 240

    for i in range(0, dims):
        for j in range(0, rows):
            for k in range(0, cols):
                img[j, k, i] = img[j, k, i] + ((mark[j, k, i] & 240) // 16)

            # img[2*j,2*k,i]=img[2*j,2*k,i]+(mark[j,k,i]&192)//64
            # img[2*j,2*k+1,i]=img[2*j,2*k+1,i]+(mark[j,k,i]&48)//16
            # img[2*j+1,2*k,i]=img[2*j+1,2*k,i]+(mark[j,k,i]&12)//4
            # img[2*j+1,2*k+1,i]=img[2*j+1,2*k+1,i]+(mark[j,k,i]&3)
    img = Image.fromarray(img)
    global new_image
    new_image = beiyinxie_image[:-4] + "_with_mark." + beiyinxie_image[-3:]

    img.save(new_image)

    tkinter.messagebox.showinfo('提示', '图像隐写已完成,隐写后的图像保存为' + new_image)

    old = cv2.imread(beiyinxie_image)
    new = cv2.imread(new_image)

    b, g, r = cv2.split(old)
    old = cv2.merge([r, g, b])
    b, g, r = cv2.split(new)
    new = cv2.merge([r, g, b])

    plt.figure(figsize=(6, 7))  # matplotlib设置画面大小 600*700
    # plt.suptitle('LSB信息隐藏')
    plt.subplot(2, 2, 1)
    plt.imshow(old)
    plt.title("原始图像")
    plt.subplot(2, 2, 2)
    plt.hist(old.ravel(), 256, [0, 256])
    plt.title("原始图像直方图")
    plt.subplot(2, 2, 3)
    plt.imshow(new)
    plt.title("隐藏信息的图像")
    plt.subplot(2, 2, 4)
    plt.hist(new.ravel(), 256, [0, 256])
    plt.title("隐藏信息图像直方图")
    plt.tight_layout()  # 设置默认的间距
    plt.show()


# 图像降级
def Image_tiqu():
    tkinter.messagebox.showinfo('提示', '请选择要进行提取图片水印的图像')
    Fpath = filedialog.askopenfilename()
    new_image = Fpath

    tkinter.messagebox.showinfo('提示', '请选择将提取信息保存的位置')
    tiqu = filedialog.askdirectory()
    # print(tiqu)

    tiqu = tiqu + '/mark_get.' + new_image[-3:]

    imgwmark = np.array(Image.open(new_image))
    result = imgwmark
    rows, cols, dims = imgwmark.shape
    rows = rows // 2
    cols = cols // 2
    for i in range(0, dims):
        for j in range(0, rows * 2):
            for k in range(0, cols * 2):
                result[j, k, i] = (imgwmark[j, k, i] & 15)
                result[j, k, i] = result[j, k, i] * 16

    mark_get = Image.fromarray(result)
    mark_get.save(tiqu)

    tkinter.messagebox.showinfo('提示', '水印图片已提取,请查看mark_get.' + new_image[-3:])


def func_LSB_suijijiange_yinxie(str1, str2, str3):
    im = Image.open(str1)
    global width, height
    width = im.size[0]
    print("width:" + str(width) + "\n")
    height = im.size[1]
    print("height:" + str(height) + "\n")
    count = 0
    # 获取需要隐藏的信息
    global keylen
    key = get_key(str2)
    keylen = len(key)
    print(key)
    print(keylen)

    random.seed(2)
    global LSB_suijijiange_step
    step_max = int(width * height / keylen)
    print('step: ', LSB_suijijiange_step)
    print('step_max: ', step_max)
    LSB_suijijiange_step = int(LSB_suijijiange_step)
    if LSB_suijijiange_step > step_max:
        tkinter.messagebox.showinfo('提示', '步长设置过大，请重新设置，步长最大值为: ' + str(step_max))
        global LSB_suijijiange_sf
        LSB_suijijiange_sf = False
        return

    step = LSB_suijijiange_step
    random_seq = [0] * keylen
    for i in range(0, keylen):
        random_seq[i] = int(random.random() * step + 1)
        print(random_seq[i])

    q = 1

    for count in range(keylen):
        w, h = q_converto_wh(q)
        pixel = im.getpixel((w, h))
        pixel = pixel - mod(pixel, 2) + int(key[count])
        q = q + random_seq[count]
        im.putpixel((w, h), pixel)

    im.save(str3)
    tkinter.messagebox.showinfo('提示', '图像隐写已完成,隐写后的图像保存为' + str3)


def LSB_suijijiange_yinxie():
    tkinter.messagebox.showinfo('提示', '请选择要进行LSB随机间隔隐写的图像')
    Fpath = filedialog.askopenfilename()
    shutil.copy(Fpath, './')

    old = Fpath.split('/')[-1]

    if (os.path.exists('./' + old) == False):
        shutil.copy(Fpath, './')
    # 处理后输出的图片路径
    new = old[:-4] + "_LSB-random_interval-generated." + old[-3:]

    # 需要隐藏的信息
    tkinter.messagebox.showinfo('提示', '请选择要隐藏的信息(请选择txt文件)')
    txtpath = filedialog.askopenfilename()
    shutil.copy(txtpath, './')
    enc = txtpath.split('/')[-1]

    if (os.path.exists('./' + enc) == False):
        shutil.copy(txtpath, './')
    # print(enc)
    global LSB_suijijiange_sf
    LSB_suijijiange_sf = True
    func_LSB_suijijiange_yinxie(old, enc, new)
    print('LSB_suijijiange_sf: ', LSB_suijijiange_sf)

    global LSB_new
    LSB_new = new

    old = cv2.imread(old)
    new = cv2.imread(new)

    if LSB_suijijiange_sf == True:
        plt.figure(figsize=(6, 7))  # matplotlib设置画面大小 600*700
        # plt.suptitle('LSB信息隐藏')
        plt.subplot(2, 2, 1)
        plt.imshow(old)
        plt.title("原始图像")
        plt.subplot(2, 2, 2)
        plt.hist(old.ravel(), 256, [0, 256])
        plt.title("原始图像直方图")
        plt.subplot(2, 2, 3)
        plt.imshow(new)
        plt.title("隐藏信息的图像")
        plt.subplot(2, 2, 4)
        plt.hist(new.ravel(), 256, [0, 256])
        plt.title("隐藏信息图像直方图")
        plt.tight_layout()  # 设置默认的间距
        plt.show()


# le为所要提取的信息的长度，str1为加密载体图片的路径，str2为提取文件的保存路径
def func_LSB_suijijiange_tiqu(le, str1, str2):
    a = ""
    b = ""
    im = Image.open(str1)

    global width
    global height
    width = im.size[0]
    height = im.size[1]
    print(width, ',', height)
    len_total = le
    count = 0
    # print(len_total)
    random.seed(2)
    # step = int(width*height/len_total)
    step = int(LSB_suijijiange_step)
    random_seq = [0] * len_total
    for i in range(0, len_total):
        random_seq[i] = int(random.random() * step + 1)

    q = 1
    count = 0

    for count in range(len_total):
        w, h = q_converto_wh(q)
        pixel = im.getpixel((w, h))
        # print(q,'-----',w,',',h)
        b = b + str(mod(pixel, 2))
        # print(count)
        q = q + random_seq[count]
        count += 1

    print(b)

    with open(str2, "wb") as f:
        for i in range(0, len(b), 8):
            # 以每8位为一组二进制，转换为十进制
            stra = toasc(b[i:i + 8])
            # stra = b[i:i+8]
            # 将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
            stra = chr(stra)
            sb = bytes(stra, encoding="utf8")
            # print(sb)
            # f.write(chr(stra))
            f.write(sb)
            stra = ""
    f.closed


def LSB_suijijiange_tiqu():
    global LSB_suijijiange_text_len
    le = int(LSB_suijijiange_text_len)
    print('le: ', le)

    tkinter.messagebox.showinfo('提示', '请选择要进行LSB随机间隔算法提取的图像')
    Fpath = filedialog.askopenfilename()

    tkinter.messagebox.showinfo('提示', '请选择将提取信息保存的位置')
    tiqu = filedialog.askdirectory()
    # print(tiqu)
    tiqu = tiqu + '/LSB-random_interval-recover.txt'
    LSB_new = Fpath
    print(LSB_new)
    func_LSB_suijijiange_tiqu(le, LSB_new, tiqu)
    tkinter.messagebox.showinfo('提示', '隐藏信息已提取,请查看LSB-random_interval-recover.txt')


def func_LSB_quyujiaoyan_yinxie(str1, str2, str3):
    im = Image.open(str1)
    # 获取图片的宽和高
    global width, height
    width = im.size[0]
    print("width:" + str(width) + "\n")
    height = im.size[1]
    print("height:" + str(height) + "\n")
    count = 0
    # 获取需要隐藏的信息
    global keylen
    key = get_key(str2)
    keylen = len(key)
    print(key)
    print(keylen)

    q = 1

    global LSB_quyujiaoyan_size
    size = int(LSB_quyujiaoyan_size)
    print('size: ', size)
    print(int(width * height / keylen))

    # LSB_suijijiange_step = int(LSB_suijijiange_step)
    # if LSB_suijijiange_step > step_max:
    size_max = int(width * height / keylen)
    print('size_max: ', size_max)
    if width * height < size * keylen:
        tkinter.messagebox.showinfo('提示', 'size设置过大，请重新设置，size最大值为: ' + str(int(width * height / keylen)))

    pixel = []
    for p in range(1, keylen + 1):
        for i in range(1, size + 1):
            w, h = q_converto_wh((p - 1) * size + i)
            print(w, h)
            # e = im.getpixel(0,1)
            pixel.append(im.getpixel((w, h)))

        tem = 0
        for i, v in enumerate(pixel):
            tem = tem + mod(v, 2)  # +mod(pixel2,2)+mod(pixel3,2)+mod(pixel4,2)
        pixel = []
        tem = mod(tem, 2)

        if tem != int(key[p - 1]):
            q = int(random.random() * size) + 1
            w, h = q_converto_wh((p - 1) * size + q)
            pix = im.getpixel((w, h))
            im.putpixel((w, h), pix - 1)

    im.save(str3)
    tkinter.messagebox.showinfo('提示', '图像隐写已完成,隐写后的图像保存为' + str3)


def LSB_quyujiaoyan_yinxie():
    tkinter.messagebox.showinfo('提示', '请选择要进行LSB区域校验位隐写的图像')
    Fpath = filedialog.askopenfilename()

    old = Fpath.split('/')[-1]

    if (os.path.exists('./' + old) == False):
        shutil.copy(Fpath, './')
    # 处理后输出的图片路径
    new = old[:-4] + "_LSB-regional_verification-generated." + old[-3:]

    # 需要隐藏的信息
    tkinter.messagebox.showinfo('提示', '请选择要隐藏的信息(请选择txt文件)')
    txtpath = filedialog.askopenfilename()
    enc = txtpath.split('/')[-1]

    if (os.path.exists('./' + enc) == False):
        shutil.copy(txtpath, './')

    # print(enc)
    func_LSB_quyujiaoyan_yinxie(old, enc, new)

    global LSB_new
    LSB_new = new

    old = cv2.imread(old)
    new = cv2.imread(new)

    plt.figure(figsize=(6, 7))  # matplotlib设置画面大小 600*700
    # plt.suptitle('LSB信息隐藏')
    plt.subplot(2, 2, 1)
    plt.imshow(old)
    plt.title("原始图像")
    plt.subplot(2, 2, 2)
    plt.hist(old.ravel(), 256, [0, 256])
    plt.title("原始图像直方图")
    plt.subplot(2, 2, 3)
    plt.imshow(new)
    plt.title("隐藏信息的图像")
    plt.subplot(2, 2, 4)
    plt.hist(new.ravel(), 256, [0, 256])
    plt.title("隐藏信息图像直方图")
    plt.tight_layout()  # 设置默认的间距
    plt.show()


# le为所要提取的信息的长度，str1为加密载体图片的路径，str2为提取文件的保存路径
def func_LSB_quyujiaoyan_tiqu(le, str1, str2):
    a = ""
    b = ""
    im = Image.open(str1)

    global width
    global height
    width = im.size[0]
    height = im.size[1]
    print(width, ',', height)
    len_total = le
    count = 0

    global LSB_quyujiaoyan_size
    size = int(LSB_quyujiaoyan_size)
    print('size: ', size)

    pixel = []
    for p in range(1, len_total + 1):
        for i in range(1, size + 1):
            w, h = q_converto_wh((p - 1) * size + i)
            pixel.append(im.getpixel((w, h)))

        re = 0
        for i, v in enumerate(pixel):
            re = re + mod(v, 2)
        pixel = []
        re = mod(re, 2)
        b = b + str(re)

    print(b)

    with open(str2, "wb") as f:
        for i in range(0, len(b), 8):
            # 以每8位为一组二进制，转换为十进制
            stra = toasc(b[i:i + 8])
            # stra = b[i:i+8]
            # 将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
            stra = chr(stra)
            sb = bytes(stra, encoding="utf8")

            f.write(sb)
            stra = ""
    f.closed


def LSB_quyujiaoyan_tiqu():
    global LSB_quyujiaoyan_text_len
    le = int(LSB_quyujiaoyan_text_len)
    print('le: ', le)

    tkinter.messagebox.showinfo('提示', '请选择要进行LSB区域校验位算法提取的图像')
    Fpath = filedialog.askopenfilename()

    tkinter.messagebox.showinfo('提示', '请选择将提取信息保存的位置')
    tiqu = filedialog.askdirectory()

    tiqu = tiqu + '/LSB-regional_verification-recover.txt'

    LSB_new = Fpath
    func_LSB_quyujiaoyan_tiqu(le, LSB_new, tiqu)
    tkinter.messagebox.showinfo('提示', '隐藏信息已提取,请查看LSB-regional_verification-recover.txt')


def DCT_trans(gray_img):
    height, width = gray_img.shape
    gray_img = gray_img.astype(float)
    img_dct = cv2.dct(gray_img)
    # 记录正负矩阵
    dct_flag = np.ones((height, width))
    for h_i in range(height):
        for w_i in range(width):
            if img_dct[h_i, w_i] < 0:
                dct_flag[h_i, w_i] = -1
    # 取log，并进行归一化
    img_dct_log = np.log(1 + abs(img_dct))
    dct_max = np.max(img_dct_log)
    dct_min = np.min(img_dct_log)
    img_dct_log255 = np.zeros((height, width), np.uint8)
    for h_i in range(height):
        for w_i in range(width):
            img_dct_log255[h_i, w_i] = (img_dct_log[h_i, w_i] - dct_min) / (dct_max - dct_min) * 255

    return img_dct_log255, dct_flag, dct_max, dct_min

def IDCT_trans(img_dct_log_wm, dct_flag, dct_max, dct_min):
    height, width = img_dct_log_wm.shape
    img_dct_log_wm = img_dct_log_wm.astype(float)
    for h_i in range(height):
        for w_i in range(width):
            img_dct_log_wm[h_i, w_i] = img_dct_log_wm[h_i, w_i] / 255 * (dct_max - dct_min) + dct_min
    img_dct_wm = (np.exp(img_dct_log_wm) - 1) * dct_flag
    img_idct_wm = cv2.idct(img_dct_wm)
    img_idct_wm = img_idct_wm.astype(np.uint8)

    return img_idct_wm

def FFT_trans(gray_img):
    height, width = gray_img.shape
    img_fft2 = np.fft.fft2(gray_img)
    img_fft2_shift = np.fft.fftshift(img_fft2)
    # 对shift归一化
    fft2_flag = img_fft2_shift / abs(img_fft2_shift)
    # 取log，并归一化到0-255
    img_fft2_log = np.log(1 + np.abs(img_fft2_shift))
    fft2_max = np.max(img_fft2_log)
    fft2_min = np.min(img_fft2_log)
    img_fft2_log255 = np.zeros((height, width), np.uint8)
    for h_i in range(height):
        for w_i in range(width):
            img_fft2_log255[h_i, w_i] = (img_fft2_log[h_i, w_i] - fft2_min) / (fft2_max - fft2_min) * 255

    return img_fft2_log255, fft2_flag, fft2_max, fft2_min


def IFFT_trans(img_fft2_log_wm, fft2_flag, fft2_max, fft2_min):
    height, width = img_fft2_log_wm.shape
    img_fft2_log_wm = img_fft2_log_wm.astype(complex)
    for h_i in range(height):
        for w_i in range(width):
            img_fft2_log_wm[h_i, w_i] = img_fft2_log_wm[h_i, w_i] / 255 * (fft2_max - fft2_min) + fft2_min
    img_fft2_shift_wm = np.exp(img_fft2_log_wm) - 1
    img_fft2_shift_wm = fft2_flag * abs(img_fft2_shift_wm)
    img_fft2_wm = np.fft.ifftshift(img_fft2_shift_wm)
    img_ifft2_wm = abs(np.fft.ifft2(img_fft2_wm))
    img_ifft2_wm = img_ifft2_wm.astype(np.uint8)

    return img_ifft2_wm


def insert_watermarkb(host_image, watermark_image):
    # key_size = 8x8
    height, width = host_image.shape[:2]  # 确定 高度height 宽度width 便于 水印尺寸进行调节

    watermark_image = cv2.resize(watermark_image, (width, height))  # 对插入的水印进行缩放，使得 水印的尺寸 适合 host

    for i in range(watermark_image.shape[0]):  # 对水印图像进行黑白化处理
        for j in range(watermark_image.shape[1]):
            if watermark_image[i][j] > 127:
                watermark_image[i][j] = 1
            else:
                watermark_image[i][j] = 0
    # cv2.imshow('demo1',watermark_image)
    block_size = 8  # 分块大小

    sub_image_x = width // block_size
    sub_image_y = height // block_size

    host_blocks = []  # host的分块
    watermark_blocks = []  # 水印的分块
    host_blocks_lsb = []  # host分块的最低有效位
    watermarked_blocks = []  # 被上了水印之后的分块

    for i in range(sub_image_y):  # 进行分块以后的两重循环，x与y都已经对blocksize整除
        for j in range(sub_image_x):
            x0 = j * block_size
            y0 = i * block_size
            x1 = x0 + block_size
            y1 = y0 + block_size

            sub_image = host_image[y0:y1, x0:x1]  # 进行图像的分割，按照blocksize分割
            host_blocks.append(sub_image)

            sub_image = watermark_image[y0:y1, x0:x1]
            watermark_blocks.append(sub_image)

    host_blocks_lsb = host_blocks  # 先把 整个 载体分块 给 lsb载体
    # print(host_blocks_lsb) 8*8
    for host_block_lsb, watermark_block in zip(host_blocks_lsb,
                                               watermark_blocks):  # zip把 host_blocks_lsb 与 watermark_blocks 打包成一一对应的对象
        for i in range(host_block_lsb.shape[0]):
            for j in range(host_block_lsb.shape[1]):
                if (host_block_lsb[i][j] % 2) != 0:  # 如果是奇数，减一变成偶数 把所有最低位的1 变成 0
                    host_block_lsb[i][j] -= 1
                    # print(host_block_lsb[i][j])
        ########################################################################################################################################
        host_block_bytes = host_block_lsb.tobytes()  # 转成字节图片数据转换完成后的二进制数据。
        # print(host_block_bytes)
        m = hashlib.md5()  # 获取一个算法加密对象
        m.update(host_block_bytes)  # 用提供的字节串更新此哈希对象(hash object)的状态。
        hash = m.digest()  # 返回摘要值,以二进制字节串的形式。
        # print(hash)
        host_block_hash_bits = ''.join(f'{b:08b}' for b in hash)  # 将字符串转成二进制字符串
        # print(host_block_hash_bits)
        # print(666)
        first_64_bit_of_hash = host_block_hash_bits[:64]  # 取出前六十四位的哈希
        #   print(first_64_bit_of_hash)
        flattened_watermark_block = watermark_block.flatten()  # 降维
        # 加密对象（host blocks lsb）  -- 二进制数据 -- 变成哈希对象 -- 返回摘要值 二进制字节串 -- 转成二进制字符串
        XOR_of_hash_and_watermark = []
        for i in range(64):
            XOR_of_hash_and_watermark.append(XOR(flattened_watermark_block[i], int(
                first_64_bit_of_hash[i])))  # 降维的水印 与  加密后的host blocks lsb 异或  相当于把水印插入
            # print(flattened_watermark_block)

        # print(XOR_of_hash_and_watermark)
        XOR_of_hash_and_watermark_array = np.reshape(XOR_of_hash_and_watermark, (8, 8))  # 8*8的规格

        for i in range(8):
            for j in range(8):
                if XOR_of_hash_and_watermark_array[i][j] == 1:  # 如果值为1 说明 降维的水印 与 加密后的host blocks lsb 不同
                    host_block_lsb[i][j] += 1  # 那么host block lsb +1

        watermarked_blocks.append(host_block_lsb)  # 加入到最终的产品

    watermarked_image = np.zeros((host_image.shape[0], host_image.shape[1]),
                                 dtype=np.uint8)  # 创造一个全0数组，参数是hostimage的长和宽，类型是0~255的整数 区别在于

    k = 0
    for i in range(sub_image_y):  # 对y//blocksize之后的大小
        for j in range(sub_image_x):
            x0 = j * block_size
            y0 = i * block_size
            x1 = x0 + block_size
            y1 = y0 + block_size

            watermarked_image[y0:y1, x0:x1] = watermarked_blocks[k]  # 把一位的blocks块给到
            k += 1

    return watermarked_image

def trace_insert(host_image, watermark_image):
    bImg, gImg, rImg = cv2.split(host_image)
    watermarked_image1 = insert_watermarkb(bImg, watermark_image)  # 得到加上水印后的图片
    watermarked_image2 = insert_watermarkb(gImg, watermark_image)
    watermarked_image3 = insert_watermarkb(rImg, watermark_image)
    imgMerge = cv2.merge([watermarked_image1, watermarked_image2, watermarked_image3])
    return imgMerge

def extract_watermark(watermarked_image):
    height, width = watermarked_image.shape[:2]

    block_size = 8

    sub_image_x = width // block_size
    sub_image_y = height // block_size

    watermarked_blocks = []  # 被上了水印的图片
    extracted_watermark_blocks = []  # 回溯的水印

    for i in range(sub_image_y):
        for j in range(sub_image_x):
            x0 = j * block_size
            y0 = i * block_size
            x1 = x0 + block_size
            y1 = y0 + block_size

            sub_image = watermarked_image[y0:y1, x0:x1]
            watermarked_blocks.append(sub_image)  # 每一个元素是一个8*8的小块图片

    watermarked_blocks_lsb = watermarked_blocks  # 进行8*8分块后的 被加了水印的 图像数组
    watermark_blocks = []
    # print(watermarked_blocks_lsb)
    for watermarked_block_lsb, watermarked_block in zip(watermarked_blocks_lsb, watermarked_blocks):
        lsbs_of_watermarked = []
        for i in range(watermarked_block_lsb.shape[0]):  # 第一层循环 8次  #8*8
            for j in range(watermarked_block_lsb.shape[1]):  # 第二层循环 8次
                if (watermarked_block_lsb[i][j] % 2) != 0:  # 如果最低位是1
                    lsbs_of_watermarked.append(1)  #这个是我们的最低位信息，如果最低位是1则在新的block中添加1这个元素
                    watermarked_block_lsb[i][j] -= 1  # 把最低位1去除，进行之后的异或操作
                else:
                    lsbs_of_watermarked.append(0) #如果最低位是0，把0添加到新的block中
                    # print(watermarked_block_lsb.shape[0])
                    # print(watermarked_block_lsb.shape[1])
        # print(lsbs_of_watermarked)
        #################################################################################################################
        watermarked_block_bytes = watermarked_block_lsb.tobytes()
        m = hashlib.md5()
        m.update(watermarked_block_bytes)
        hash = m.digest()
        watermarked_block_hash_bits = ''.join(f'{b:08b}' for b in hash)

        first_64_bit_of_hash = watermarked_block_hash_bits[:64]#对图片（可能被篡改，可能没被篡改）进行哈希映射，取前64位

        XOR_of_hash_and_watermark = []
        for i in range(64):
            XOR_of_hash_and_watermark.append(XOR(lsbs_of_watermarked[i], int(first_64_bit_of_hash[i])))#对每一位进行异或，接下来有两种情况
            #在此回忆一下水印是如何得到的。我们取host,记为I，最低位全部清零（I0），然后进行哈希映射取前64位H(I0)
            #记水印watermark为W
            #用H(I0) XOR W ，结果放入 watermarked 的最低位 ，这样函数返回了 watermarked了 . watermarked 与 host 的不同点在于最低有效位
            #记为 H(I0) XOR W == I @ W(最低位)
            #两边再同时异或H（I0）得到  W == I @ W（最低位） XOR H(I0)
            #I0 @ W 最低位可能被篡改 把结果记为 (I0 @ W 最低位)'
            #（I0 @ W 最低位）' XOR H(I @ W ’| 最低位置0) -->  水印
            #情况1 在某个block中 I @ W (最低位) 没有被篡改，那么H（I0） 也没有被篡改， 因此这个 block 中水印保持原样
            #情况2 在某个block中 I @ W （最低位） 被篡改， 那么对应的哈希映射被篡改，与此同时 H（I0）也必将被篡改， 因此这个block 中 水印会出现“大便”一样的噪点，这样的噪点就实现了篡改的检测
        watermark_block = XOR_of_hash_and_watermark

        watermark_block = np.reshape(watermark_block, (8, 8))

        for i in range(8):
            for j in range(8):
                if watermark_block[i][j] == 1:#由于我们的水印只有黑（0）与白（255），因此如果水印block的某一位是1，那么它代表的是亮度255的白
                    watermark_block[i][j] = 255

        watermark_blocks.append(watermark_block)

    extracted_watermark_image = np.zeros((watermarked_image.shape[0], watermarked_image.shape[1]),
                                         dtype=np.uint8)  # 创建一个和水印图像一样规格的 全0数组

    k = 0
    #把一维排列的水印结果复原成二维图像
    for i in range(sub_image_y):
        for j in range(sub_image_x):
            x0 = j * block_size
            y0 = i * block_size
            x1 = x0 + block_size
            y1 = y0 + block_size

            extracted_watermark_image[y0:y1, x0:x1] = watermark_blocks[k]  # 回溯的水印
            #  0  0  <-- x x
            #  0  0  <-- x x
            k += 1

    return extracted_watermark_image  # 回溯的水印

def trace_extract(watermarked_image):
    bImg, gImg, rImg = cv2.split(watermarked_image)

    extracted_watermark1 = extract_watermark(bImg)
    extracted_watermark2 = extract_watermark(gImg)
    extracted_watermark3 = extract_watermark(rImg)
    imgMerge1 = cv2.merge([extracted_watermark1, extracted_watermark2, extracted_watermark3])
    return imgMerge1


# 图像篡改
def img_tamper(img):
    img_temper = img
    height, width, _ = img_temper.shape
    x1 = random.randrange(int(height / 4), int(height / 3))
    y1 = random.randrange(int(width / 4), int(width / 3))
    x2 = random.randrange(x1 + 1, int(height / 2))
    y2 = random.randrange(y1 + 1, int(width / 2))
    print("Tampered area: (" + str(x1) + "," + str(y1) + "), (" + str(x2) + "," + str(y2) + ")")
    img_part = img_temper[x1:x2, y1:y2]
    gaussian_img = cv2.GaussianBlur(img_part, (3, 3), 0)
    img_temper[x1:x2, y1:y2] = gaussian_img
    return img_temper


def FFT_insert(img_fft2_log255, gray_water_mark):
    height, width = img_fft2_log255.shape
    height2, width2 = gray_water_mark.shape
    # 改变插入水印的大小
    new_size = (int(height2 * (width / (5 * width2))), int(width / 5))
    new_h = new_size[0]
    new_w = new_size[1]
    gray_water_mark = cv2.resize(gray_water_mark, (new_w, new_h))
    for h_i in range(new_h):
        for w_i in range(new_w):
            if gray_water_mark[h_i, w_i] < 50:
                img_fft2_log255[h_i, w_i] = gray_water_mark[h_i, w_i]
    gray_water_mark180 = np.rot90(gray_water_mark, 2)
    for h_i in range(new_h):
        for w_i in range(new_w):
            if gray_water_mark180[h_i, w_i] < 50:
                img_fft2_log255[height - new_h + h_i, width - new_w + w_i] = gray_water_mark180[h_i, w_i]
    img_fft2_log_wm = img_fft2_log255

    return img_fft2_log_wm

def DCT_insert(img_dct_log255, gray_water_mark):
    height, width = img_dct_log255.shape
    height2, width2 = gray_water_mark.shape
    # 改变插入水印的大小
    new_size = (int(height2 * (width / (5 * width2))), int(width / 5))
    new_h = new_size[0]
    new_w = new_size[1]
    gray_water_mark = cv2.resize(gray_water_mark, (new_w, new_h))
    for h_i in range(new_h):
        for w_i in range(new_w):
            if gray_water_mark[h_i, w_i] < 10:
                img_dct_log255[height - new_h + h_i, width - new_w + w_i] = 50
    img_idct_log_wm = img_dct_log255

    return img_idct_log_wm

def Change_Detect(gray_change, img_idct_wm):
    height, width = img_idct_wm.shape
    gray_change = gray_change.astype(float)
    change_dct = cv2.dct(gray_change)
    change_dct_log = np.log(1 + abs(change_dct))
    dct_max = np.max(change_dct_log)
    dct_min = np.min(change_dct_log)
    change_dct_log255 = np.zeros((height, width), np.uint8)
    for h_i in range(height):
        for w_i in range(width):
            change_dct_log255[h_i, w_i] = (change_dct_log[h_i, w_i] - dct_min) / (dct_max - dct_min) * 255

    return change_dct_log255 - img_idct_wm