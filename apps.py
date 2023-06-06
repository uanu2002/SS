import tkinter.messagebox  # 弹窗库
from tkinter.ttk import *
from algorithm import *
import tkinter.font as tkFont
import numpy as np
from tkinter import *
from tkinter import ttk
from functools import partial

np.set_printoptions(suppress=True)
plt.rcParams['font.sans-serif'] = ['SimHei']
rootdir = "./tmp/"


def create_random_interval():
    root = Toplevel()
    root.title("随机间隔法")
    width = 800
    height = 400
    set_center(root, width, height)
    Label(root, text="随机间隔法", font=fontStyle1).pack()

    button5 = Button(root, text="LSB随机间隔法水印嵌入", command=LSB_suijijiange_yinxie)  # 控制label的颜色
    button6 = Button(root, text="LSB随机间隔法水印提取", command=LSB_suijijiange_tiqu)  # 控制label的颜色
    button5.place(height=60, width=350, x=30, y=150)
    button6.place(height=60, width=350, x=430, y=150)
    myentry = Entry(root)
    myentry.place(x=350, y=65)

    def get_entry_text():
        global LSB_suijijiange_step
        LSB_suijijiange_step = myentry.get()
        tkinter.messagebox.showinfo('提示', '随机间隔步长已被设置为 ' + LSB_suijijiange_step)
        print('LSB_suijijiange_step: ', LSB_suijijiange_step)

    Button(root, text="设置随机间隔的步长", command=get_entry_text).place(x=357, y=87.5)

    myentry1 = Entry(root)
    myentry1.place(x=350, y=300)

    def get_entry_text():
        global LSB_suijijiange_text_len
        LSB_suijijiange_text_len = myentry1.get()
        tkinter.messagebox.showinfo('提示', '输入提取信息的长度已被设置为 ' + LSB_suijijiange_text_len)
        print(LSB_suijijiange_text_len)

    Button(root, text="输入提取信息的长度", command=get_entry_text).place(x=350, y=320)

    Message(root
            ,
            text='∎随机间隔法水印嵌入由用户选择图片和隐藏信息\n∎对图像进行随机间隔的LSB隐写后，将秘密信息写入\n∎绘制原始图像和隐写后的图像的直方图对比，并保存隐写后的图像\n∎随机间隔的步长由用户输入').place \
        (x=100, y=230)
    Message(root, text='∎随机间隔法水印提取由用户选择要提取信息的图片和提取信息的保存路径\n∎程序将使用同样的随机种子，读取随机间隔法水印嵌入时保存的图像并提取出信息并保存到用户选择的路径').place \
        (x=530, y=230)

    root.mainloop()


def creatre_regional_verification():
    root = Toplevel()
    root.title("区域校验位算法")
    width = 850
    height = 400
    set_center(root, width, height)
    Label(root, text="区域校验位算法", font=fontStyle1).pack()

    button5 = Button(root, text="LSB区域校验位算法水印嵌入", command=LSB_quyujiaoyan_yinxie)
    button6 = Button(root, text="LSB区域校验位算法水印提取", command=LSB_quyujiaoyan_tiqu)
    button5.place(height=60, width=370, x=30, y=150)
    button6.place(height=60, width=370, x=430, y=150)

    myentry = Entry(root)
    myentry.place(x=350, y=55)

    def get_entry_text():
        global LSB_quyujiaoyan_size
        LSB_quyujiaoyan_size = myentry.get()
        tkinter.messagebox.showinfo('提示', '区域大小已被设置为 ' + LSB_quyujiaoyan_size)
        print(LSB_quyujiaoyan_size)

    Button(root, text="请输入区域校验位参数(区域大小)", command=get_entry_text).place(x=330, y=78)

    myentry1 = Entry(root)
    myentry1.place(x=330, y=300)

    def get_entry_text():
        global LSB_quyujiaoyan_text_len
        LSB_quyujiaoyan_text_len = myentry1.get()
        tkinter.messagebox.showinfo('提示', '输入提取信息的长度已被设置为 ' + LSB_quyujiaoyan_text_len)
        print(LSB_quyujiaoyan_text_len)

    Button(root, text="输入提取信息的长度", command=get_entry_text).place(x=335, y=323)

    Message(root
            ,
            text='∎区域校验位算法水印嵌入由用户选择图片和隐藏信息\n∎对图像进行区域校验位的LSB隐写后，将秘密信息写入\n∎绘制原始图像和隐写后的图像的直方图对比，并保存隐写后的图像\n∎区域校验位算法的区域大小由用户输入').place \
        (x=100, y=230)
    Message(root, text='∎区域校验位算法水印提取由用户选择要提取信息的图片和提取信息的保存路径\n∎读取区域校验位算法水印嵌入时保存的图像并提取出信息并保存到用户选择的路径').place(x=550, y=230)

    root.mainloop()


# 图像降级
def create_image():
    root = Toplevel()

    root.title("图片水印")
    width = 700
    height = 400
    set_center(root, width, height)

    w = Canvas(root)
    w.place(x=300, y=0, width=300, height=700)
    w.create_line(180, 50, 180, 330,
                  fill='#C0C0C0',
                  # fill='red',
                  width=2, )

    Message(root
            , text='∎图像降级算法水印嵌入由用户选择载体图片和水印图片\n∎将载体图片的四个最低为比特位替换成水印图片的四个最高比特位\n∎绘制原始图像和隐写后的图像的直方图对比，并保存隐写后的图像').place \
        (x=500, y=60)
    Message(root, text='∎图像降级算法水印提取由用户选择要提取信息的图片和提取信息的保存位置\n∎程序读取要提取信息的图片，提取出隐藏的图片并保存').place(x=500, y=230)
    Label(root, text="图像降级算法", font=fontStyle).pack()
    button5 = Button(root, text="图像降级算法水印嵌入", command=Image_yinxie)  # 控制label的颜色
    button6 = Button(root, text="图像降级算法水印提取", command=Image_tiqu)  # 控制label的颜色
    button5.place(height=60, width=300, x=150, y=80)
    button6.place(height=60, width=300, x=150, y=230)
    root.mainloop()


# 图像降级改进
def create_image1():
    root = Toplevel()
    root.title("图片水印")
    width = 700
    height = 400
    set_center(root, width, height)

    w = Canvas(root)
    w.place(x=300, y=0, width=300, height=700)
    w.create_line(205, 50, 205, 330,
                  fill='#C0C0C0',
                  # fill='red',
                  width=2, )

    Message(root
            , text='∎图像降级算法改进水印嵌入由用户选择载体图片和水印图片\n∎将水印图片的信息的八位的二进制数分成四块，每块分别加入到载体图片上去\n∎绘制原始图像和隐写后的图像的直方图对比，并保存隐写后的图像'
            , cursor='cross', width='150').place(x=520, y=60)
    Message(root, text='∎图像降级算法改进水印提取由用户选择要提取信息的图片和提取信息的保存位置\n∎程序读取要提取信息的图片，提取出隐藏的图片并保存', cursor='cross'
            , width='150').place(x=520, y=230)

    Label(root, text="图像降级算法改进", font=fontStyle).pack()
    button5 = Button(root, text="图像降级算法改进水印嵌入", command=Image1_yinxie)  # 控制label的颜色
    button6 = Button(root, text="图像降级算法改进水印提取", command=Image1_tiqu)  # 控制label的颜色
    button5.place(height=60, width=350, x=130, y=60)
    button6.place(height=60, width=350, x=130, y=230)
    root.mainloop()


def create_LSB_improve():
    root = Toplevel()
    root.title("LSB算法改进")
    width = 800
    height = 400
    set_center(root, width, height)

    w = Canvas(root)
    w.place(x=300, y=0, width=300, height=700)
    w.create_line(290, 100, 290, 300,
                  fill='#C0C0C0',
                  # fill='red',
                  width=2, )

    Label(root, text="LSB算法改进", font=fontStyle1).pack()
    button7 = Button(root, text="LSB随机间隔法", command=create_random_interval)  # 控制label的颜色
    button9 = Button(root, text="LSB区域校验位算法", command=creatre_regional_verification)  # 控制label的颜色

    button7.place(height=60, width=350, x=200, y=100)
    button9.place(height=60, width=350, x=200, y=200)
    Message(root, text='LSB随机间隔法包括随机间隔法水印嵌入和随机间隔水印提取', cursor='cross', width='150').place(x=600, y=100)
    Message(root, text='LSB区域校验位算法包括区域校验位算法水印嵌入和区域校验位算法水印提取', cursor='cross', width='150').place(x=600, y=200)
    root.mainloop()


def create_image_downgrade():
    root = Toplevel()
    root.title("图像降级算法及其改进")
    width = 800
    height = 400
    set_center(root, width, height)

    w = Canvas(root)
    w.place(x=300, y=0, width=300, height=700)
    w.create_line(280, 100, 280, 300,
                  fill='#C0C0C0',
                  # fill='red',
                  width=2, )

    Label(root, text="图像降级算法及其改进", font=fontStyle1).pack()
    button7 = Button(root, text="图像降级算法", command=create_image)  # 控制label的颜色
    button9 = Button(root, text="图像降级算法改进", command=create_image1)  # 控制label的颜色

    button7.place(height=60, width=350, x=200, y=100)
    button9.place(height=60, width=350, x=200, y=200)
    Message(root, text='图像降级算法包括图像降级算法水印嵌入和图像降级算法水印提取').place(x=600, y=100)
    Message(root, text='图像降级算法改进包括图像降级算法改进水印嵌入和图像降级算法改进水印提取').place(x=600, y=200)

    root.mainloop()


def create_LSB_basic():
    root = Toplevel()
    root.title("LSB基本算法")
    width = 800
    height = 400
    set_center(root, width, height)
    w = Canvas(root)
    w.place(x=300, y=0, width=300, height=700)
    w.create_line(290, 50, 290, 330,
                  fill='#C0C0C0',
                  width=2, )

    button1 = Button(root, text="LSB基本算法水印嵌入", command=LSB_yinxie)
    button2 = Button(root, text="LSB基本算法水印提取", command=LSB_tiqu)

    button1.place(height=60, width=300, x=250, y=50)
    button2.place(height=60, width=300, x=250, y=200)

    Message(root, text='∎LSB基本算法水印嵌入由用户选择图片和隐藏信息\n∎对图像进行最低有效位隐写后将秘密信息写入\n∎绘制原始图像和隐写后的图像的直方图对比，并保存隐写后的图像'
            , cursor='cross', width='150').place(x=600, y=50)
    Message(root, text='∎LSB基本算法水印提取由用户选择要提取信息的图片和提取信息的保存路径\n∎程序将读取LSB隐写时保存的图像并提取出信息，保存到用户选择的路径', cursor='cross'
            , width='150').place(x=600, y=200)

    myentry = Entry(root)
    myentry.place(x=320, y=300)

    def get_entry_text():
        global LSB_text_len
        LSB_text_len = myentry.get()
        tkinter.messagebox.showinfo('提示', '提取信息长度已被设置为 ' + LSB_text_len)
        print(LSB_text_len)

    Button(root, text="输入提取信息的长度", command=get_entry_text).place(x=320, y=320)

    Label(root, text="LSB基本算法", font=fontStyle1).pack()

    root.mainloop()


def create_DCT(Root):
    root = Toplevel(Root)

    Label(root, text="变换域水印", font=fontStyle1).pack()
    root.title("变换域水印")
    width = 700
    height = 400
    set_center(root, width, height)
    button3 = Button(root, text="DCT水印嵌入", command=DCT_yinxie)  # 控制label的边界
    button4 = Button(root, text="DCT水印提取", command=DCT_tiqu)  # 控制label的颜色
    button3.place(height=60, width=200, x=100, y=150)
    button4.place(height=60, width=200, x=400, y=150)

    Message(root, text='∎DCT水印嵌入由用户选择图片和隐藏信息\n∎对图像进行DCT变换后将秘密信息写入\n∎绘制原始图像和隐写后的图像的直方图对比，并保存隐写后的图像', cursor='cross',
            width='150').place(x=100, y=250)
    Message(root, text='∎DCT提取由用户选择要提取信息的图片和提取信息的保存路径\n∎程序将读取DCT隐写时保存的图像并提取出信息并保存到用户选择的路径', cursor='cross',
            width='150').place(x=430, y=250)

    myentry = Entry(root)
    myentry.place(x=280, y=300)

    def get_entry_text():
        global DCT_text_len
        DCT_text_len = myentry.get()
        tkinter.messagebox.showinfo('提示', '提取信息长度已被设置为' + DCT_text_len)
        print(DCT_text_len)

    Button(root, text="输入提取信息的长度", command=get_entry_text).place(x=280, y=330)

    root.mainloop()


def create_LSB(Root):
    root1 = Toplevel(Root)
    root1.title("空间域水印")
    width = 800
    height = 430
    set_center(root1, width, height)
    w = Canvas(root1)
    w.place(x=300, y=0, width=300, height=700)
    w.create_line(250, 50, 250, 370,
                  fill='#C0C0C0',
                  width=2, )

    Label(root1, text="空间域水印").pack()
    button2 = Button(root1, text="LSB基本算法", command=create_LSB_basic)
    button0 = Button(root1, text="LSB算法改进", command=create_LSB_improve)
    button7 = Button(root1, text='图像降级算法及其改进', command=create_image_downgrade)

    Message(root1, text='∎LSB基本算法包括LSB基本算法水印嵌入和LSB基本算法水印提取.\n∎可以实现将信息隐藏在图片中和从隐藏信息的图片中提取信息的功能', cursor='cross'
            , width='150').place(x=600, y=50)
    Message(root1, text='∎LSB算法改进包括随机间隔法和区域校验位算法\n∎在LSB算法的基础上，减小了水印嵌入对载体图片统计特性的影响', cursor='cross', width='150').place \
        (x=600, y=170)
    Message(root1, text='∎图像降级算法及其改进包括图像降级算法和图像降级算法的改进\n∎可以实现将图片水印嵌入图片当中的功能', cursor='cross', width='150').place(x=600
                                                                                                                 ,
                                                                                                                 y=300)

    button2.place(height=60, width=300, x=200, y=50)
    button0.place(height=60, width=300, x=200, y=170)
    button7.place(height=60, width=300, x=200, y=300)

    root1.mainloop()


class WatermarkSystem:
    def __init__(self):
        self.root = Tk()
        self.root.title("信号与系统")
        window_width = 1000
        window_height = 800
        set_center(self.root, window_width, window_height)
        self.root.attributes('-toolwindow', False, '-alpha', 0.9, '-fullscreen', False, '-topmost', False)
        global fontStyle, fontStyle1, fontStyle2
        fontStyle = tkFont.Font(family="Lucida Grande", size=20)
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=15)
        fontStyle2 = tkFont.Font(family="Lucida Grande", size=10)
        self.fontStyle = fontStyle
        self.fontStyle2 = fontStyle2

        self.create_widgets()

    def create_widgets(self):
        self.w = Canvas(self.root)
        self.w.place(x=500, y=170, width=300, height=190)

        Label(self.root, text="基于数字图像的可视化水印系统", font=self.fontStyle).pack()

        self.style = ttk.Style()
        self.style.configure("TButton", font=self.fontStyle)
        self.style.configure("Test.TButton", font=self.fontStyle2)
        Button(self.root, text='空间域水印', command=self.create_LSB).place(height=60, width=100, x=100, y=170)
        Button(self.root, text='变换域水印', command=self.create_DCT).place(height=60, width=100, x=250, y=170)
        Button(self.root, text='新功能按钮', command=self.create_new_function).place(height=60, width=100, x=400, y=170)

        Message(self.root, text='空间域水印包含:\n    LSB水印嵌入和提取\n    LSB算法改进\n    图像降级算法及其改进',
                cursor='heart', width='200').place(x=100, y=270, width=150)
        Message(self.root, text='变换域水印包含:\n    DCT隐写\n    DCT提取', cursor='heart', width='200').place(x=250, y=270,
                                                                                                     width=150)

        Message(self.root, text='新功能:\n    描述1\n    描述2\n', cursor='heart', width='200').place(x=400, y=270, width=150)

    def create_LSB(self):
        create_LSB(self.root)

    def create_DCT(self):
        create_DCT(self.root)

    def create_new_function(self):
        create_DCT(self.root)

    def mainloop(self):
        self.root.mainloop()


class WatermarkSystem2:
    def __init__(self):
        self.root = Tk()
        self.root.title("信号与系统")
        window_width = 1200
        window_height = 800
        set_center(self.root, window_width, window_height)
        self.root.attributes('-toolwindow', False, '-alpha', 0.9, '-fullscreen', False, '-topmost', False)
        global fontStyle, fontStyle1, fontStyle2
        fontStyle = tkFont.Font(family="Lucida Grande", size=20)
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=15)
        fontStyle2 = tkFont.Font(family="Lucida Grande", size=10)
        self.fontStyle = fontStyle
        self.fontStyle2 = fontStyle2
        self.img_origin_path = "./tmp/image.png"
        self.mask_path = rootdir + "defaultwm.png"
        self.img_origin = PhotoImage(file=self.img_origin_path)
        self.img_show1 = PhotoImage(file=self.img_origin_path)
        self.img_show2 = PhotoImage(file=self.img_origin_path)
        self.mask_show1 = PhotoImage(file=self.mask_path)
        self.create_widgets()

    def update_img(self, new_img, img):
        img_path = rootdir + new_img
        img.configure(file=img_path)

    def update_function_sub(self, selected_value):
        values = list()
        if selected_value == "时域分析":
            values = ["FFT时域重建", "DCT时域重建", "三维FFT时域重建", "三维DCT时域重建"]
        elif selected_value == "频域分析":
            values = ["FFT频域分析", "DCT频域分析", "三维FFT频域分析", "三维DCT频域分析"]
        elif selected_value == "水印添加":
            values = ["FFT频域水印", "DCT频域水印", "LSB时域水印", "三维FFT频域水印", "三维DCT频域水印", "文本水印"]
        elif selected_value == "篡改检测":
            values = ["篡改存在", "篡改定位", "ELA分析", "文本水印提取"]
        elif selected_value == "图像篡改":
            values = ["篡改1-高斯模糊", "篡改2-图像嫁接"]
        self.function_combobox_sub['values'] = values

    def call_method(self, selected_method):
        prefix_img_path_in = rootdir + str(self.combobox1.get())
        prefix_img_path_in2 = rootdir + str(self.combobox2.get())
        new_option = str(self.combobox1.get()) # 输出命名
        img_path_in = prefix_img_path_in + '.png'
        img_path_in2 = prefix_img_path_in2 + '.png'
        img_out = None
        print(img_path_in)
        if selected_method == "FFT频域分析":
            img_in = path2cv2(img_path_in)
            img_out, _, _, _ = FFT_trans(img_in)
            new_option = new_option + '_FFT'

        elif selected_method == "DCT频域分析":
            img_in = path2cv2(img_path_in)
            img_out, _, _, _ = DCT_trans(img_in)
            new_option = new_option + '_DCT'

        elif selected_method == "三维DCT频域分析":
            img_in = path2cv3(img_path_in)
            wm_img = path2cv3(self.mask_path)
            img_out, _, _ = DCT3_insert(img_in, wm_img)
            new_option = new_option + '_DCT3'

        elif selected_method == "三维FFT频域分析":
            img_in = path2cv3(img_path_in)
            wm_img = path2cv3(self.mask_path)
            img_out, _, _ = FFT3_insert(img_in, wm_img)
            new_option = new_option + '_FFT3'

        elif selected_method == "三维FFT频域水印":
            img_in = path2cv3(img_path_in)
            wm_img = path2cv3(self.mask_path)
            _, img_out, _ = FFT3_insert(img_in, wm_img)
            new_option = new_option + '_FFT3_marked'

        elif selected_method == "三维DCT频域水印":
            img_in = path2cv3(img_path_in)
            wm_img = path2cv3(self.mask_path)
            _, img_out, _ = DCT3_insert(img_in, wm_img)
            new_option = new_option + '_DCT3_marked'

        elif selected_method == "三维FFT时域重建":
            img_in = path2cv3(img_path_in)
            wm_img = path2cv3(self.mask_path)
            _, _, img_out = FFT3_insert(img_in, wm_img)
            new_option = new_option + '_IFFT3'

        elif selected_method == "三维DCT时域重建":
            img_in = path2cv3(img_path_in)
            wm_img = path2cv3(self.mask_path)
            _, _, img_out = DCT3_insert(img_in, wm_img)
            new_option = new_option + '_IDCT3'

        elif selected_method == "FFT时域重建":
            parts = prefix_img_path_in.rsplit("_", 1)[0]
            parts = parts.split("_", 1)
            img_path_in0 = parts[0] + '.png'
            img_in0 = path2cv2(img_path_in0)
            img_in = path2cv2(img_path_in)
            img_fft2_log_wm, fft2_flag, fft2_max, fft2_min = FFT_trans(img_in0)
            img_out = IFFT_trans(img_in, fft2_flag, fft2_max, fft2_min)
            new_option = new_option + '_IFFT'

        elif selected_method == "DCT时域重建":
            parts = prefix_img_path_in.rsplit("_", 1)[0]
            parts = parts.split("_", 1)
            img_path_in0 = parts[0] + '.png'
            img_in0 = path2cv2(img_path_in0)
            img_in = path2cv2(img_path_in)
            img_dct_log255, dct_flag, dct_max, dct_min = DCT_trans(img_in0)
            img_out = IDCT_trans(img_in, dct_flag, dct_max, dct_min)
            new_option = new_option + '_IDCT'

        elif selected_method == "FFT频域水印":
            img_in = path2cv2(img_path_in)
            wm_img = path2cv2(self.mask_path)
            img_in, _, _, _ = FFT_trans(img_in)
            img_out = FFT_insert(img_in, wm_img)
            new_option = new_option + '_FFT_marked'

        elif selected_method == "DCT频域水印":
            img_in = path2cv2(img_path_in)
            wm_img = path2cv2(self.mask_path)
            img_in, _, _, _ = DCT_trans(img_in)
            img_out = DCT_insert(img_in, wm_img)
            new_option = new_option + '_DCT_marked'

        elif selected_method == "篡改存在":
            img_in = path2cv2(img_path_in)
            img_in2 = path2cv2(img_path_in2)
            img_out = Change_Detect(img_in2, img_in)
            new_option = new_option + '_diff'

        elif selected_method == "LSB时域水印":
            host_image = cv2.imread(img_path_in, 1)

            # host_image = bImg   # 选择host
            watermark_image = cv2.imread(self.mask_path, 0)  # 选择水印
            img_out = trace_insert(host_image, watermark_image)
            new_option = new_option + '_Trace_marked'

        elif selected_method == "篡改定位":
            watermarked_image = cv2.imread(img_path_in, 1)
            img_out = trace_extract(watermarked_image)
            new_option = new_option + '_Trace_extrated'

        elif selected_method == "ELA分析":
            img_out = convert_to_ela_image(img_path_in, quality=90)
            new_option = new_option + '_ELA'
            img_path_out = rootdir + new_option + '.png'
            img_out.save(img_path_out, 'PNG', quality=90)
            self.add_combobox_option(self.combobox2, new_option)
            self.add_combobox_option(self.combobox1, new_option)
            self.update_img(str(new_option) + '.png', self.img_show2)
            return

        elif selected_method == "文本水印提取":
            txt_out = DCT_txt_extract(img_path_in)
            self.entry.insert(0, txt_out)
            return

        elif selected_method == "文本水印":
            self.add_wm_txt()
            return

        elif selected_method == "篡改1-高斯模糊":
            self.add_tamper()
            return

        elif selected_method == "篡改2-图像嫁接":
            self.add_wm_img()
            return

        img_path_out = rootdir + new_option + '.png'
        print(img_path_out)
        cv2.imwrite(img_path_out, img_out)
        self.add_combobox_option(self.combobox2, new_option)
        self.add_combobox_option(self.combobox1, new_option)
        self.update_img(str(new_option) + '.png', self.img_show2)

    def on_select1(self, event):
        selected_value = self.combobox1.get()
        self.update_img(str(selected_value) + '.png', self.img_show1)
        print(f"Selected1: {selected_value}")

    def on_select2(self, event):
        selected_value = self.combobox2.get()
        self.update_img(str(selected_value) + '.png', self.img_show2)
        print(f"Selected2: {selected_value}")

    def on_select_function(self, event):
        selected_value = self.function_combobox.get()
        self.update_function_sub(selected_value)
        print(f"Selected_function: {selected_value}")

    def on_select_function_sub(self, event):
        selected_value = self.function_combobox_sub.get()
        self.call_method(selected_value)
        print(f"Selected_function_sub: {selected_value}")

    def add_combobox_option(self, combobox, new_option):
        values = list(combobox['values'])
        if new_option in values:
            values.remove(new_option)
        combobox['values'] = values + [new_option]
        print('Add combobox option')

    def delete_combobox_option(self, combobox, selected_option):
        values = list(combobox['values'])
        values.remove(selected_option)  # 从选项列表中移除选中的选项
        combobox['values'] = values

    def add_wm_img(self):
        # 图像篡改1
        prefix_img_path_in = rootdir + str(self.combobox1.get())
        new_option = str(self.combobox1.get()) + '_out'
        img_path_in = prefix_img_path_in + '.png'
        img_in = cv2.imread(img_path_in, 1)
        img_out = img_tamper2(img_in)
        new_option = new_option + '_Tampered2'
        img_path_out = rootdir + new_option + '.png'
        print(img_path_out)
        cv2.imwrite(img_path_out, img_out)
        self.add_combobox_option(self.combobox2, new_option)
        self.add_combobox_option(self.combobox1, new_option)
        self.update_img(str(new_option) + '.png', self.img_show2)

    def add_wm_txt(self):
        txt = self.entry.get()
        txt = str(txt)
        prefix_img_path_in = rootdir + str(self.combobox1.get())
        img_path_in = prefix_img_path_in + '.png'
        new_option = str(self.combobox1.get()) + '_out'
        img_out = DCT_txt_insert(img_path_in, txt)
        print(txt)
        new_option = new_option + '_txt_marked'
        img_path_out = rootdir + new_option + '.png'
        print(img_path_out)
        cv2.imwrite(img_path_out, img_out)
        self.add_combobox_option(self.combobox2, new_option)
        self.add_combobox_option(self.combobox1, new_option)
        self.update_img(str(new_option) + '.png', self.img_show2)

    def add_tamper(self):
        prefix_img_path_in = rootdir + str(self.combobox1.get())
        new_option = str(self.combobox1.get()) + '_out'
        img_path_in = prefix_img_path_in + '.png'
        img_in = cv2.imread(img_path_in, 1)
        img_out = img_tamper(img_in)
        new_option = new_option + '_Tampered1'
        img_path_out = rootdir + new_option + '.png'
        print(img_path_out)
        cv2.imwrite(img_path_out, img_out)
        self.add_combobox_option(self.combobox2, new_option)
        self.add_combobox_option(self.combobox1, new_option)
        self.update_img(str(new_option) + '.png', self.img_show2)

    def resize(self, event):
        # 在窗口大小调整时调用此函数
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        # 计算新的组件位置
        label_x = window_width // 2
        label_y = window_height // 2
        self.img_container1.place(x=window_width // 30, y=30 + 20)
        self.img_container2.place(x=label_x + window_width // 30, y=30 + 20)
        self.combobox1.place(x= window_width // 30, y=480)
        self.combobox2.place(x=label_x + window_width // 30, y= 480)
        self.function_combobox.place(x=window_width // 30, y=530)
        self.function_combobox_sub.place(x=window_width // 30, y=630)
        self.img_container3.place(x=label_x + window_width // 30 + 50, y=window_height // 30 + 450)
        # self.wm_img_button.place(height=60, width=100, x=window_width // 2 + 30, y=600)
        # self.wm_txt_button.place(height=60, width=100, x=window_width // 2 + 30, y=500)
        self.entry.place(x=window_width // 2 + 30, y=550)
        # self.tamper_button.place(height=60, width=100, x=window_width // 2 + 30, y=700)


    def create_widgets(self):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        Label(self.root, text="基于数字水印的图片篡改检测系统", font=self.fontStyle).pack()
        self.root.bind("<Configure>", self.resize)

        # 创建标签并显示图片
        self.img_container1 = Label(self.root, image=self.img_show1, width=400, height=400)
        self.img_container2 = Label(self.root, image=self.img_show2, width=400, height=400)
        self.img_container1.place(x=30, y=50)
        self.img_container2.place(x=width // 2 + 30, y=50)
        self.img_container3 = Label(self.root, image=self.mask_show1, width=400, height=400)
        self.img_container3.place(x=width // 2 + 30, y=400)

        init_images = ["image", "mark", "liftingbody", "peppers", "saturn", "text"]
        self.combobox1 = ttk.Combobox(self.root, values=init_images)
        self.combobox1.configure(width=50, font=('Arial', 12, 'bold'))
        self.combobox1.current(0)
        self.combobox1.bind("<<ComboboxSelected>>", self.on_select1)
        self.combobox1.place(x=30, y=470)

        self.combobox2 = ttk.Combobox(self.root, values=init_images)
        self.combobox2.configure(width=50, font=('Arial', 12, 'bold'))
        self.combobox2.current(0)
        self.combobox2.bind("<<ComboboxSelected>>", self.on_select2)
        self.combobox2.place(x=width // 2 + 30, y=470)

        # self.wm_txt_button = Button(self.root, text='文本水印', command=self.add_wm_txt)
        # self.wm_txt_button.place(height=60, width=100, x=width // 2 + 30, y=500)
        # self.wm_img_button = Button(self.root, text='图像篡改1', command=self.add_wm_img)
        # self.wm_img_button.place(height=60, width=100, x=width // 2 + 30, y=600)
        # self.tamper_button = Button(self.root, text='图像篡改2', command=self.add_tamper)
        # self.tamper_button.place(height=60, width=100, x=width // 2 + 30, y=700)

        self.entry = Entry(self.root)
        self.entry.place(x=width // 2 + 30, y=550)

        self.function_combobox = ttk.Combobox(self.root, values=["时域分析", "频域分析", "水印添加", "图像篡改", "篡改检测"])
        self.function_combobox.configure(width=30, font=('Arial', 12, 'bold'))
        self.function_combobox.current(0)
        self.function_combobox.bind("<<ComboboxSelected>>", self.on_select_function)
        self.function_combobox.place(x=30, y=500)

        self.function_combobox_sub = ttk.Combobox(self.root, values=[])
        self.function_combobox_sub.configure(width=30, font=('Arial', 12, 'bold'))
        self.function_combobox_sub.bind("<<ComboboxSelected>>", self.on_select_function_sub)
        self.function_combobox_sub.place(x=30, y=600)
        # img_container1.pack()
        # Button(self.root, text='空间域水印', command=self.create_LSB).place(height=60, width=100, x=100, y=170)
        # Button(self.root, text='变换域水印', command=self.create_DCT).place(height=60, width=100, x=250, y=170)
        # Button(self.root, text='新功能按钮', command=self.create_new_function).place(height=60, width=100, x=400, y=170)
        #
        # Message(self.root, text='空间域水印包含:\n    LSB水印嵌入和提取\n    LSB算法改进\n    图像降级算法及其改进',
        #         cursor='heart', width='200').place(x=100, y=270, width=150)
        # Message(self.root, text='变换域水印包含:\n    DCT隐写\n    DCT提取', cursor='heart', width='200').place(x=250, y=270,
        #                                                                                              width=150)
        #
        # Message(self.root, text='新功能:\n    描述1\n    描述2\n', cursor='heart', width='200').place(x=400, y=270, width=150)

    def create_LSB(self):
        create_LSB(self.root)

    def create_DCT(self):
        create_DCT(self.root)

    def create_new_function(self):
        create_DCT(self.root)

    def mainloop(self):
        self.root.mainloop()
