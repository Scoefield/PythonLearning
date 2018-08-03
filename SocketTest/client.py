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
host = socket.gethostname()
# 设置端口号
port = 9999

# 连接服务，指定主机和端口
s.connect((host, port))

if __name__ == '__main__':
    # 接收小于 1024 字节的数据
    msg = s.recv(1024)
    s.close()

    print(msg.decode('utf-8'))