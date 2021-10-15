import socket  # 导入 socket 模块
from threading import Thread
import datetime
import traceback
import json
import random
import csv

class Server:
    """
    服务端主类
    """
    __user_cls = None

    @staticmethod
    def write_log(msg):
        cur_time = datetime.datetime.now()
        s = "[" + str(cur_time) + "]" + msg
        print(s)

    def __init__(self, ip, port):
        self.connections = []  # 所有客户端连接
        self.write_log('Server opening，please waiting...')
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 监听者，用于接收新的socket连接
            self.listener.bind((ip, port))  # 绑定ip、端口
            self.listener.listen(5)  # 最大等待数
        except:
            self.write_log('Server fail to open，please check if there is collide of ip end.Detail Information：\n' + traceback.format_exc())

        if self.__user_cls is None:
            self.write_log('Server fail to open!')
            return

        self.write_log('Server run successfully：{}:{}'.format(ip,port))
        while True:
            client, _ = self.listener.accept()  # 阻塞，等待客户端连接
            user = self.__user_cls(client, self.connections)
            self.connections.append(user)
            self.write_log('New connection enter，the current number of connection：{}'.format(len(self.connections)))

    @classmethod
    def register_cls(cls, sub_cls):
        """
        注册玩家的自定义类
        """
        if not issubclass(sub_cls, Connection):
            cls.write_log('Register do not match')
            return

        cls.__user_cls = sub_cls


class Connection:
    """
    连接类，每个socket连接都是一个connection
    """

    def __init__(self, socket, connections):
        self.socket = socket
        self.connections = connections
        self.data_handler()

    def data_handler(self):
        # 给每个连接创建一个独立的线程进行管理
        thread = Thread(target=self.recv_data)
        thread.setDaemon(True)
        thread.start()

    def recv_data(self):
        # 接收数据
        try:
            while True:
                bytes = self.socket.recv(2048)  # 我们这里只做一个简单的服务端框架，不去做分包处理。所以每个数据包不要大于2048
                if len(bytes) == 0:
                    self.socket.close()
                    # 删除连接
                    self.connections.remove(self)
                    break
                # 处理数据
                self.deal_data(bytes)
        except:
            self.connections.remove(self)
            Server.write_log('Some user\'s connection have terminated：\n' + traceback.format_exc())

    def deal_data(self, bytes):
        """
        处理客户端的数据，需要子类实现
        """
        raise NotImplementedError



class Player(Connection):
    """
    玩家类，我们的游戏中，每个连接都是一个Player对象
    """
    def __init__(self, *args):
        self.login_state = False  # 登录状态
        self.game_data = None  # 玩家游戏中的相关数据
        self.log = {'user1':'111111','user2':'222222','user3':'333333','user4':'444444'}
        self.connect_num = 0
        super().__init__(*args)

    def deal_data(self, bytes):# 接收data
        """
        处理服务端发送的数据
        :param bytes:
        :return:
        """
        bytes = eval(bytes.decode('utf8').split('|#|')[0]) #传过来的data
        if bytes['protocol'] == 'connect':

                data = {
                'protocol': 'connect',
                'number' : len(self.connections)
                }# 传回来 第几个玩家

                self.send_self(data)
        # byte【protocol】 register 写文件操作 新账号密码 两个新的elif（两个新protocol名字） :
        # 一个登录（读写操作和判断 加judge）sens_self(data)一个注册（写文件）
        elif bytes['protocol']=='login':#登录
            filename = 'data.csv'
            dic_data={}
            with open(filename) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    username = row['username']
                    password= row['password']
                    # print(username)
                    # print(password)
                    dic_data[username]=password
            if bytes['username'] in dic_data and dic_data[bytes['username']] == bytes['password']:
                reply = {
                'protocol': 'login-reply',
                'number' : len(self.connections),
                'judge':1
                    # 说明账户密码对不对
                }# 传回来 第几个玩家

                self.send_self(reply)
        elif bytes['protocol']=='signup':#注册
            judge=1
            filename = 'data.csv'
            dic_data={}
            with open(filename) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    username = row['username']
                    password= row['password']
                    # print(username)
                    # print(password)
                    dic_data[username]=password
            if bytes['username'] in dic_data:
                judge=0
                #玩家用户名已存在
            if judge==1:
                with open(r'data.csv',mode='a',newline='',encoding='utf8') as cfa:
                    wf = csv.writer(cfa)
                    data2 = [[bytes['username'],bytes['password']]]
                    for i in data2:
                        wf.writerow(i)
            reply2 = {
                'protocol': 'signup-reply',
                'number' : len(self.connections),
                'judge':judge
                }
            self.send_self(reply2)

        elif bytes['protocol'] == 'ready':
            """
            {
                'protocol':'ready'
            }
            """
            data = {
                'protocol':'ready'
            }
            self.send_without_self(data)
        elif bytes['protocol'] == 'running':
            """
            {
                'protocol':'running',
                'cur_number':'1',
                'move_chess':'1',
                'step':'1'
                'if_final':'0'
            }
            """
            step = bytes['step']
            data = {
                'protocol': 'running',
                'step':step,
                'cur_number':bytes['cur_number'],
                'move_chess':bytes['move_chess'],
                'if_final': bytes['if_final']
                }
            self.send_without_self(data)
        print('\nInformation：',bytes)

    def send(self, py_obj):
        """
        给玩家发送协议包
        py_obj:python的字典或者list
        """
        self.socket.sendall((json.dumps(py_obj, ensure_ascii=False) + '|#|').encode())

    def send_all_player(self, py_obj):
        """
        把这个数据包发送给所有在线玩家，包括自己
        """
        for player in self.connections:
            player.send(py_obj)

    def send_without_self(self, py_obj):
        """
        发送给除了自己的所有在线玩家
        """
        for player in self.connections:
            if player is not self :
                player.send(py_obj)

    def send_self(self, py_obj):
        for player in self.connections:
            if player is self :
                player.send(py_obj)

Server.register_cls(Player)
Server('127.0.0.1', 6666)


