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
        self.img_origin_path = filedialog.askopenfilename()
        self.img_origin = PhotoImage(file=self.img_origin_path)
        self.img_show1 = PhotoImage(file=self.img_origin_path)
        self.img_show2 = PhotoImage(file=self.img_origin_path)
        self.create_widgets()


    def update_img(self, new_img, img):
        img_path = rootdir + new_img
        img.configure(file=img_path)

    def update_function_sub(self, selected_value):
        values = list()
        if selected_value == "图像分析":
            values = ["时域分析", "FFT频域分析", "DCT频域分析"]

        elif selected_value == "水印添加":
            values = ["时域水印添加", "频域水印添加"]
        elif selected_value == "篡改检测":
            values = ["篡改存在", "篡改定位"]
        self.function_combobox_sub['values'] = values

    def call_method(self, selected_method):
        prefix_img_path_in = rootdir + str(self.combobox1.get())
        new_option = str(self.combobox1.get()) + '_out'
        img_path_in = prefix_img_path_in + '.png'

        if selected_method == "FFT频域分析":
            pass
        elif selected_method == "DCT频域分析":
            img_in = path2cv2(img_path_in)
            img_out = DCT_trans(img_in)
            new_option = new_option + '_DCT'
            img_path_out = rootdir + new_option + '.png'
            print(img_path_out)
            cv2.imwrite(img_path_out, img_out)

        self.add_combobox_option(self.combobox2, new_option)
        self.update_img(str(new_option)+'.png', self.img_show2)
        img_path_out = prefix_img_path_in + '_'



    def on_select1(self, event):
        selected_value = self.combobox1.get()
        self.update_img(str(selected_value)+'.png', self.img_show1)
        print(f"Selected1: {selected_value}")

    def on_select2(self, event):
        selected_value = self.combobox2.get()
        self.update_img(str(selected_value)+'.png', self.img_show2)
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
        combobox['values'] = list(combobox['values']) + [new_option]
        print('123')

    def delete_combobox_option(self, combobox, selected_option):
        values = list(combobox['values'])
        values.remove(selected_option)  # 从选项列表中移除选中的选项
        combobox['values'] = values

    def create_widgets(self):
        Label(self.root, text="基于数字图像的可视化水印系统", font=self.fontStyle).pack()

        self.style = ttk.Style()

        # 创建标签并显示图片
        self.img_container1 = Label(self.root, image=self.img_show1, width=400, height=400)
        self.img_container2 = Label(self.root, image=self.img_show2, width=400, height=400)
        self.img_container1.place(x=30, y=30)
        self.img_container2.place(x=500+30, y=30)

        self.combobox1 = ttk.Combobox(self.root, values=["image", "mark", "Option 3"])
        self.combobox1.current(0)
        self.combobox1.bind("<<ComboboxSelected>>", self.on_select1)
        self.combobox1.place(x=30, y=440)

        self.combobox2 = ttk.Combobox(self.root, values=["image", "mark", "Option 3"])
        self.combobox2.current(0)
        self.combobox2.bind("<<ComboboxSelected>>", self.on_select2)
        self.combobox2.place(x=500+30, y=440)

        self.function_combobox = ttk.Combobox(self.root, values=["图像分析", "水印添加", "篡改检测"])
        self.function_combobox.current(0)
        self.function_combobox.bind("<<ComboboxSelected>>", self.on_select_function)
        self.function_combobox.place(x=30, y=500)

        self.function_combobox_sub = ttk.Combobox(self.root, values=[])
        self.function_combobox_sub.bind("<<ComboboxSelected>>", self.on_select_function_sub)
        self.function_combobox_sub.place(x=30, y=550)
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
