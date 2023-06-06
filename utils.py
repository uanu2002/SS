import random
import cv2


def plus(str):
    return str.zfill(8)


# Python zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。

def get_key(strr):
    # 获取要隐藏的文件内容
    tmp = strr
    f = open(tmp, "rb")
    str = ""
    s = f.read()
    global text_len
    text_len = len(s)
    for i in range(len(s)):
        # code.interact(local=locals())
        str = str + plus(bin(s[i]).replace('0b', ''))
    # 逐个字节将要隐藏的文件内容转换为二进制，并拼接起来
    # 1.先用ord()函数将s的内容逐个转换为ascii码
    # 2.使用bin()函数将十进制的ascii码转换为二进制
    # 3.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空
    # 4.又由于ascii码转换二进制后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位
    # print str
    f.closed
    return str


def get_key_str(strr):
    str = ""
    s = strr
    text_len = len(s)
    for i in range(len(s)):
        # code.interact(local=locals())
        str = str + plus(bin(ord(s[i])).replace('0b', ''))
    # 逐个字节将要隐藏的文件内容转换为二进制，并拼接起来
    # 1.先用ord()函数将s的内容逐个转换为ascii码
    # 2.使用bin()函数将十进制的ascii码转换为二进制
    # 3.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空
    # 4.又由于ascii码转换二进制后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位
    # print str
    return str


def mod(x, y):
    return x % y;


def toasc(strr):
    return int(strr, 2)


# q转换成第几行第几列
# width行height列
def q_converto_wh(q):
    w = q // 600
    h = q % 600
    return w, h


def swap(a, b):
    return b, a


def randinterval(m, n, count, key):
    # m,n = matrix.shape
    print(m, n)
    interval1 = int(m * n / count) + 1
    interval2 = interval1 - 2
    if interval2 == 0:
        print('载体太小，不能将秘密信息隐藏进去!')
    # print('interval1:', interval1)
    # print('interval2:', interval2)

    # 生成随机序列
    random.seed(key)
    a = [0] * count  # a是list
    for i in range(0, count):
        a[i] = random.random()

    # 初始化
    row = [0] * count
    col = [0] * count

    # 计算row和col
    r = 0
    c = 0
    row[0] = r
    col[0] = c
    for i in range(1, count):
        if a[i] >= 0.5:
            c = c + interval1
        else:
            c = c + interval2
        if c > n:
            k = c % n
            r = r + int((c - k) / n)
            if r > m:
                print('载体太小不能将秘密信息隐藏进去!')
            c = k
            if c == 0:
                c = 1
        row[i] = r
        col[i] = c

    return row, col


def set_center(root, width, height):
    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 窗口的宽度和高度
    window_width = width
    window_height = height

    # 计算窗口的左上角坐标，使其居中显示在屏幕上
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # 设置窗口的初始位置
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")


def path2cv2(img_path):
    img = cv2.imread(img_path)
    cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2img


def path2cv3(img_path):
    img = cv2.imread(img_path)
    return img


def XOR(bit1, bit2):
    if bit1 == bit2:
        return 0
    else:
        return 1
