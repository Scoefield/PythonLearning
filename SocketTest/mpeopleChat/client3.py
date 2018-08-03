#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: client3.py
@time: 2018/4/21 22:05
"""
import socket
import sys
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import client2

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# count = 0

def connect():
    # 获取要连接的主机地址
    host = entry1.get()
    # 获取端口号
    port = int(entry2.get())
    # 连接服务，指定主机和端口
    s.connect((host, port))
    # 接收连接状态提示消息
    msg = s.recv(1024).decode('utf-8')
    scr1.insert("insert", msg)
    # global count
    # count += 1

def btnsend():
    # 获取要发送的消息
    sendmsg = entry3.get()
    if sendmsg == '':
        messagebox.showwarning("Warning", "发送的内容不能为空")
    else:
        s.send(sendmsg.encode('utf-8'))
        entry3.delete(0, END)
        msg = s.recv(1024).decode('utf-8')
        scr1.insert("insert", msg)

    # client2.client2Insert()

def client1Insert():
    msg = s.recv(1024).decode('utf-8')
    print("进来client1了")
    scr1.insert("insert", msg)

def clientUI():
    root = Tk()
    root.title("ClientThree")  # 标题
    root.geometry("560x500")  # 窗口大小

    Label(root, text="服务器IP：").grid(row=0, column=0, padx=8, pady=10)
    global sfile, entry1
    sfile = StringVar()
    entry1 = Entry(root, textvariable=sfile, width=20)
    entry1.grid(row=0, column=1, padx=2, pady=10)

    Label(root, text="端口号：").grid(row=0, column=2, padx=10, pady=10)
    global sfile2, entry2
    sfile2 = StringVar()
    entry2 = Entry(root, textvariable=sfile2, width=20)
    entry2.grid(row=0, column=3, padx=2, pady=10)

    Button(root, text="连接", width=8, command=connect).grid(row=0, column=4, padx=8, pady=10)

    # Label(root, text="").grid(row=1)  # 这里插入一个标签，相当于换行
    Label(root,
          text="-------------------------------------------------------------------------------------------------------------") \
        .grid(row=1, columnspan=5)  # 这里插入一个空的标签，相当于换行
    Label(root, text="消息显示：").grid(row=2, column=0, padx=20)
    scrolW = 58
    scrolH = 20
    global scr1
    scr1 = scrolledtext.ScrolledText(root, width=scrolW, height=scrolH, wrap=WORD)
    scr1.grid(row=3, column=0, columnspan=5, padx=12)

    Label(root,
          text="-------------------------------------------------------------------------------------------------------------")\
        .grid(row=4, columnspan=5)  # 这里插入一个标签，相当于换行
    Label(root, text="").grid(row=5, columnspan=5)
    Label(root, text="写消息：").grid(row=6, column=0)
    global sfile3, entry3
    sfile3 = StringVar()
    entry3 = Entry(root, textvariable=sfile3, width=50)
    entry3.grid(row=6, column=1, columnspan=3)
    Button(root, text="发送", width=8, command=btnsend).grid(row=6, column=4)

    # if count != 0:
    #     recevie()

    root.mainloop()


def main():
    msg = s.recv(1024)
    print(msg.decode('utf-8'))
    sendmsg = input("请输入：")
    s.send(sendmsg.encode('utf-8'))

    msg2 = s.recv(1024)
    print(msg2.decode('utf-8'))

if __name__ == '__main__':
    # main()
    clientUI()