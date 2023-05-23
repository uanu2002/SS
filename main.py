from tkinter import *

root = Tk()  # 创建一个主窗体。相当于提供了一个搭积木的桌子
from apps import *

np.set_printoptions(suppress=True)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签

# center_window(root, 500, 200)
root.title("信号与系统")
# root.geometry('1100x500+200+20')#调整窗体大小,第一个数横大小，第二个数纵大小，第三个数离左屏幕边界距离，第四个数离上面屏幕边界距离
root.geometry('850x500')  # 调整窗体大小,第一个数横大小，第二个数纵大小，第三个数离左屏幕边界距离，第四个数离上面屏幕边界距离

root.attributes('-toolwindow', False,
                '-alpha', 0.9,
                '-fullscreen', False,
                '-topmost', False)

w = Canvas(root)
w.place(x=500, y=170, width=300, height=190)

Label(root, text="基于数字图像的可视化水印系统", font=fontStyle).pack()

style = Style(root)
style.configure("TButton", font=fontStyle)
style.configure("Test.TButton", font=fontStyle2)
Button(root, text='空间域水印', command=create_LSB).place(height=60, width=200, x=170, y=170)
Button(root, text='变换域水印', command=create_DCT).place(height=60, width=200, x=450, y=170)

Message(root, text='空间域水印包含:\n    LSB水印嵌入和提取\n    LSB算法改进\n    图像降级算法及其改进', cursor='cross', width='200').place(x=200,
                                                                                                               y=270,
                                                                                                               width=200)
Message(root, text='变换域水印包含:\n    DCT隐写\n    DCT提取', cursor='cross', width='200').place(x=450, y=270, width=200)

root.mainloop()  # 开启一个消息循环队列，可以持续不断地接受操作系统发过来的键盘鼠标事件，并作出相应的响应
# mainloop应该放在所有代码的最后一行，执行他之后图形界面才会显示并响应系统的各种事件
