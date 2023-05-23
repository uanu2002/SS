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
    # print('le: ',le)
    count = int(DCT_text_len)
    print('count: ', count)

    tkinter.messagebox.showinfo('提示', '请选择要进行DCT提取的图像')
    Fpath = filedialog.askopenfilename()
    dct_encoded_image_file = Fpath.split('/')[-1]

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