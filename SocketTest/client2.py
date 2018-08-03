#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: client.py
@time: 2018/4/20 13:53
"""
import socket
import sys

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
# host = socket.gethostname()
host = '127.0.0.1'
# 设置端口好
# port = 9999
port = 17170
# 连接服务，指定主机和端口
s.connect((host, port))

if __name__ == '__main__':
    # while True:
        # 接收小于 1024 字节的数据
        msg = s.recv(1024)
        print(msg.decode('utf-8'))
        sendmsg = input("请输入：")
        s.send(sendmsg.encode('utf-8'))

        msg2 = s.recv(1024)
        print(msg2.decode('utf-8'))

        # if sendmsg == 'login':
        #     loginmsg = s.recv(1024)
        #     print(loginmsg.decode('utf-8'))
        # s.close()

