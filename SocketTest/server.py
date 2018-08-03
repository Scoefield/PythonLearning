#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: server.py
@time: 2018/4/20 13:53
"""
import socket
import sys

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = socket.gethostname()
port = 9999

# 绑定端口号
serversocket.bind((host, port))

# 设置最大连接数，超过后排队
serversocket.listen(5)

def main():
    while True:
        # 建立客户端连接，等待客户端连接...
        clientsocket, addr = serversocket.accept()
        # print("clientsocket:", clientsocket)
        print("连接地址: %s" % str(addr))

        msg = '欢迎访问菜鸟网络编程！' + "\r\n"
        clientsocket.send(msg.encode('utf-8'))
        print("chulaile...")
        clientsocket.close()

if __name__ == '__main__':
    main()