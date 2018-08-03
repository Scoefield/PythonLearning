#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: serverall.py
@time: 2018/4/21 9:38
"""
#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: server.py
@time: 2018/4/20 17:22
"""
import socket
from db import DB
from threading import currentThread, Thread

class HandlerThread(object):
    queue = [] # sockect 队列
    # db = DB()

    def __init__(self, sock):
        self.sock = sock

    def recv(self):
        data = self.sock.recv(1024).strip() # 如果使用 while 接收数据时，会导致用户必须多敲一次回车键
        return data.decode('utf-8')

    def send(self, data):
        # self.sock.sendall(('[System]: %s' % data).encode('utf-8'))
        self.sock.send(data.encode('utf-8'))    # send传的是bytes，所以要要encode编码一下

    # 向队列中广播消息
    def broadcast(self, user, data):
        for sock in self.queue:
            print(sock)
            sock.sendall(('\n[%s]: %s\n' % (user, data)).encode('utf-8'))

    # 关闭客户端连接
    def stop(self):
        self.send('ByeBye!')
        self.sock.close()
        self.queue.remove(self.sock) # 关闭连接后，记得从队列中删除
        print("客户端关闭成功！")

    # 程序入口
    def handler(self):
        try:
            thname = currentThread().getName()
            print('[%s] Got connection from %s' % (thname, self.sock.getpeername())) # 打印连接信息
            self.queue.append(self.sock)  # 登录系统者，连接被加入到队列中
            self.send('创建进程[%s]并连接成功，欢迎加入聊天室！\n' % thname)

            # self.chat_room(self.sock)
            self.chat_room(thname)
        except  Exception as e:                 # 如果这里不捕获一下，就无法正常断开客户端连接
            print("发生异常！！！异常信息为：", e)

    def chat_room(self, user):
        user_data = self.recv()
        if user_data == 'exit':
            self.stop()
        elif user_data == '':
            print("空字符串！！！")
            self.send("\n发送的内容为空！")
        else:
            self.broadcast(user, user_data)
            print("出来了。。。")
            # self.send(user_data)
            self.chat_room(user)

# 为每连接创建线程
def Startthread(sock, addr):
    print('Received new client connection. %s:%s' % (addr[0], addr[1]))

    th = HandlerThread(sock)
    t = Thread(target=th.handler)
    t.setDaemon(True)
    t.start()

# 启动服务
def Server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 9999))
    s.listen(5)

    while True:
        try:
            sock, addr = s.accept()
        except KeyboardInterrupt:
            exit('\nByeBye!')

        Startthread(sock, addr)

    s.close()

if __name__ == '__main__':
    Server()