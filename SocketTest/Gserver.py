#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: Gserver.py
@time: 2018/4/20 13:40
"""
import socket
from db import DB
from threading import currentThread, Thread


class HandlerThread(object):
    queue = [] # sockect 队列
    db = DB()

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
            sock.sendall('\n[%s]: %s\n' % (user, data))

    # 关闭客户端连接
    def stop(self):
        self.send('ByeBye!')
        self.sock.close()
        self.queue.remove(self.sock) # 关闭连接后，记得从队列中删除

    # 程序入口
    def handler(self):
        funcdict = {
                    'login': self.login,
                    'register': self.register
        }
        try:
            thname = currentThread().getName()
            print('[%s] Got connection from %s' % (thname, self.sock.getpeername())) # 该程序中所有 print 的数据，将全部使用 loging 模块代替
            self.send('请输入你要选择的功能：login/register/exit')

            data = self.recv()
            # print("data:", data)
            if data == 'exit':
                self.stop() # 其实这里应该单独使用 self.sock.close() 来关闭连接，因为这时队列中并没有该连接，不过有了下面的捕获就没有问题了 ^_^
            elif data in funcdict:
                # print("jinalile...")
                return funcdict.get(data)()
            else:
                self.handler()
        except  Exception as e:                 # 如果这里不捕获一下，就无法正常断开客户端连接
            print("发生异常！！！异常信息为：", e)

    # 处理用户登陆
    def login(self):
        self.send('Login... 请输入用户名密码，格式：User Password，输入 Server: 执行程序指令！')
        user_data = self.recv()

        # 程序内部指令
        if user_data == 'Server:':
            self.send('\n\tServer:use reged\t切换到注册页\n\tServer:exit\t\t退出系统')
            user_data = self.recv()
            if user_data == 'Server:use reged':
                self.register()
            elif user_data == 'Server:exit':
                self.stop()
            else:
                self.send('输入错误...')

        datalist = user_data.split()

        # 判断用户输入，格式是否正确
        if len(datalist) == 2:
            user = datalist[0]
            password = datalist[1]

            db_data = self.db.get_data() or {}

            if user in db_data and password == db_data.get(user):
                self.queue.append(self.sock) # 有权限登陆系统者，连接被加入到队列中
                self.send('欢迎加入聊天室，输入 Server: 获取功能方法！')
                self.broadcast('System', '[%s] 加入聊天室！' % user)
                self.chat_room(user)
            else:
                self.send('用户名、密码错误！')
                self.login()
        self.login()

    def register(self):
        self.send('Register... 请输入用户名密码，格式：User Password，输入 Server: 执行程序指令！')
        user_data = self.recv()

        if user_data == 'Server:':
            self.send('\n\tServer:use login\t切换到注册页\n\tServer:exit\t\t退出系统')
            user_data = self.recv()
            if user_data == 'Server:login':
                self.login()
            elif user_data == 'Server:exit':
                self.stop()
            else:
                self.send('输入错误...')

        datalist = user_data.split()

        if len(datalist) == 2:
            user = datalist[0]
            password = datalist[1]

            db_data = self.db.get_data() or {}

            if user in db_data:
                self.send('该用户名已被注册！')
                self.register()
            else:
                db_data[user] = password
                self.db.put_data(db_data)
                self.queue.append(self.sock)
                self.broadcast('System', '新用户 [%s] 加入聊天室！' % user)
                self.chat_room(user)
        self.register()

    def chat_room(self, user):
        user_data = self.recv()
        if user_data == 'Server:':
            self.send('\n\tServer:logout\t退出聊天室')
            user_data = self.recv()
            if user_data == 'Server:logout':
                self.stop()
                return # 这里如果不加 return ，会将客户端执行的 Server: 指令也广播出去
            else:
                self.send('输入错误...')
                self.chat_room(user)
        else:
            self.broadcast(user, user_data)
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
    s.bind(('127.0.0.1', 17170))
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
