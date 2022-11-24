import tkinter as tk
from 实验一txt.test1 import *
import 实验一txt

window = tk.Tk()

window.title('12003990122-赖祥媛-实验合集')
window.geometry('1000x700')

# 创建scale进行实验的选择：
frm = tk.Frame(window, width=1000, height=700)
frm.place(x=0, y=0)
frm_l = tk.Frame(frm, width=500, height=700, bg='yellow')
frm_l.place(x=0, y=0)


def exe1():
    """实验一二"""
    t1 = text1()


menubar = tk.Menu(window)  # 创建一个新的Menu，包含实验目录
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='实验目录', menu=filemenu)
filemenu.add_command(label='实验一、二', command=exe1)
filemenu.add_command(label='实验三', )
filemenu.add_command(label='实验四', )
filemenu.add_command(label='实验五', )
filemenu.add_command(label='实验六', )
filemenu.add_command(label='实验七', )
filemenu.add_command(label='实验八', )
filemenu.add_command(label='实验九', )
window.config(menu=menubar)

window.mainloop()
