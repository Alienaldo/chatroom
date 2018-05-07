import socket
from threading import *
from time import *


class Chatroom:
    socket_list = []
    user_info = {"John": "12345"}

    def __init__(self, sock):
        self.sock = sock

    def send(self, data):
        self.sock.send(bytes(data, encoding="utf-8"))

    def recv(self):
        data = str(self.sock.recv(1024), encoding="utf-8")
        if data == "":
            print("someone is gone")
        return data

    def broadcast(self, data):
        if len(Chatroom.socket_list) > 0:
            for i in Chatroom.socket_list:
                i.send(bytes(data, encoding="utf-8"))

    def signinorup(self):
        data = self.recv()
        # 若客户端与服务器连接中断则recv函数会一直返回空字符串
        if data == "":
            print("Client Connection Close")
            return
        # 接收的数据的格式为method:username:passward
        # 按照“：”来将字符串分割
        data_list = data.split(":")
        if len(data_list) == 3:
            method = data_list[0]
            username = data_list[1]
            passward = data_list[2]
            if method == "signin":
                # 若信息与类变量user_info中的一致，则进入聊天室
                if username in Chatroom.user_info and passward == Chatroom.user_info[username]:
                    self.send("welcome")
                    self.chat(username)
                    return
                #     密码不对
                elif username in Chatroom.user_info:
                    self.send("Wrong Passward")
                else:
                    self.send("User doesn't exist, please sign up")
            elif method == "signup":
                if username in Chatroom.user_info:
                    self.send("User already exists, change another name")
                else:
                    Chatroom.user_info[username] = passward
                    self.send("Sign up Success")
        self.signinorup()
        return


    def chat(self, username):
        # 将用户加入广播的列表
        Chatroom.socket_list.append(self.sock)
        self.broadcast("welcome " + username)
        while True:
            try:
                data = self.recv()
                print("pause")
                print(data)
                self.broadcast(username + ":" + data)
            except ConnectionResetError:
                print("Connection Close")
                Chatroom.socket_list.remove(self.sock)
                self.broadcast(username + " is gone")
                self.sock.close()
                break

    def start(self):
        self.signinorup()


def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12345
    # ip地址为127.0.0.1或者域名为 字符串localhost均可在离线的情况下被同一台机子上的客户端连上
    host = "127.0.0.1"
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(5)
    while True:
        try:
            client_sock, addr = server_sock.accept()
            cr = Chatroom(client_sock)
            t = Thread(target=cr.start)
            t.start()
        except ConnectionResetError:
            print("Close Connection")
        except:
            print("Error")


if __name__ == '__main__':
    server()
