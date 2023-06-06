import tkinter.messagebox  # 弹窗库
from tkinter.ttk import *
from algorithm import *
import tkinter.font as tkFont
import numpy as np
from tkinter import *
from tkinter import ttk, messagebox
from functools import partial

np.set_printoptions(suppress=True)
plt.rcParams['font.sans-serif'] = ['SimHei']
rootdir = "./tmp/"


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
        self.mask_path2 = rootdir + "defaultwm2.png"
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
            values = ["DWT-DCT-SVD水印", "FFT频域水印", "DCT频域水印", "LSB时域水印", "三维FFT频域水印", "三维DCT频域水印", "文本水印"]
        elif selected_value == "篡改检测":
            values = ["DWT-DCT-SVD水印提取", "篡改存在", "频域水印提取", "ELA分析", "图像比对", "文本水印提取"]
        elif selected_value == "图像篡改":
            values = ["篡改1-高斯模糊", "篡改2-图像嫁接", "篡改3-图像压缩", "篡改4-裁剪攻击", "篡改5-锐化/钝化攻击"]
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

        elif selected_method == "图片比对":
            img_in = path2cv2(img_path_in)
            img_in2 = path2cv2(img_path_in2)
            img_out = Change_Detect(img_in2, img_in)
            new_option = new_option + '_diff'

        elif selected_method == "篡改存在":
            img_in = path2cv2(img_path_in)
            wm = cv2.imread(self.mask_path)
            img_out = FFT2_Detect(img_in, wm)
            messagebox.showinfo('篡改存在检测', str(img_out))
            return


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

        elif selected_method == "DWT-DCT-SVD水印":
            img_out = blind_insert(img_path_in, self.mask_path2)
            new_option = new_option + '_DDS_marked'

        elif selected_method == "DWT-DCT-SVD水印提取":
            wm = path2cv2(self.mask_path2)
            img_out = blind_extract(img_path_in, wm.shape)
            new_option = new_option + '_DDS_extracted'

        elif selected_method == "频域水印提取":
            img_in = cv2.imread(img_path_in)
            wm = cv2.imread(self.mask_path)
            img_out = Get_WM(img_in, wm)
            new_option = new_option + '_Mark_extracted'

        elif selected_method == "篡改1-高斯模糊":
            self.add_tamper()
            return

        elif selected_method == "篡改2-图像嫁接":
            self.add_wm_img()
            return

        elif selected_method == "篡改3-图像压缩":
            self.add_tamper_compress()
            return

        elif selected_method == "篡改4-裁剪攻击":
            self.add_tamper_cut()
            return

        elif selected_method == "篡改5-锐化/钝化攻击":
            self.add_tamper_blur_sharpen()
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
        new_option = str(self.combobox1.get())
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
        new_option = str(self.combobox1.get())
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

    def add_tamper_compress(self):
        prefix_img_path_in = rootdir + str(self.combobox1.get())
        new_option = str(self.combobox1.get())
        img_path_in = prefix_img_path_in + '.png'
        img_in = path2cv3(img_path_in)
        img_out = Tamper_Compress(img_in, 0.5)
        new_option = new_option + '_Tampered3'
        img_path_out = rootdir + new_option + '.png'
        print(img_path_out)
        cv2.imwrite(img_path_out, img_out)
        self.add_combobox_option(self.combobox2, new_option)
        self.add_combobox_option(self.combobox1, new_option)
        self.update_img(str(new_option) + '.png', self.img_show2)

    def add_tamper_cut(self):
        prefix_img_path_in = rootdir + str(self.combobox1.get())
        new_option = str(self.combobox1.get())
        img_path_in = prefix_img_path_in + '.png'
        img_in = path2cv3(img_path_in)
        img_out = Tamper_Cut2(img_in)
        new_option = new_option + '_Tampered4'
        img_path_out = rootdir + new_option + '.png'
        print(img_path_out)
        cv2.imwrite(img_path_out, img_out)
        self.add_combobox_option(self.combobox2, new_option)
        self.add_combobox_option(self.combobox1, new_option)
        self.update_img(str(new_option) + '.png', self.img_show2)

    def add_tamper_blur_sharpen(self):
        prefix_img_path_in = rootdir + str(self.combobox1.get())
        new_option = str(self.combobox1.get())
        img_path_in = prefix_img_path_in + '.png'
        img_in = path2cv3(img_path_in)
        img_out = Tamper_sharpen_and_blur(img_in)
        new_option = new_option + '_Tampered5'
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
        self.change_wm_button.place(height=60, width=100, x=window_width // 30, y=window_height*7//8)
        self.judge_button.place(height=60, width=100, x=window_width // 30 + 150, y=window_height*7//8)
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

        init_images = ["image", "mark", "liftingbody", "peppers", "saturn"]
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
        self.change_wm_button = Button(self.root, text='水印切换', command=self.change_wm)
        self.change_wm_button.place(height=60, width=100, x=width // 2 + 30, y=700)
        self.judge_button = Button(self.root, text='质量评估', command=self.Judge)
        self.judge_button.place(height=60, width=100, x=width // 2 + 180, y=700)

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

    def change_wm(self, image1_path = "./tmp/defaultwm.png", image2_path = "./tmp/defaultwm2.png"):
        return
        image1_name, image1_ext = os.path.splitext(image1_path)
        image2_name, image2_ext = os.path.splitext(image2_path)
        tmp = "./tmp/123.png"
        os.rename(image1_path, tmp)
        os.rename(image2_path, image1_name + image2_ext)
        os.rename(image1_path, image2_name + image1_ext)
        pass

    def Judge(self):
        prefix_img_path_in = rootdir + str(self.combobox1.get())
        prefix_img_path_in2 = rootdir + str(self.combobox2.get())
        img_path_in = prefix_img_path_in + '.png'
        img_path_in2 = prefix_img_path_in2 + '.png'
        img_in = path2cv2(img_path_in)
        img_in2 = path2cv2(img_path_in2)
        img_out = PSNR(img_in, img_in2)
        messagebox.showinfo('图像质量检测', 'PSNR: ' + str(img_out))

    def mainloop(self):
        self.root.mainloop()
