from tkinter import *
from threading import *
from time import *
import socket


class Chatroom:
    def __init__(self):
        self.username = ""
        self.passward = ""
        self.data = ""
    # 在按下connect按钮后调用
    def Connection(self, f):
        # 获取你输入的ip地址和端口号
        dest_ip = self.ip.get()
        dest_port = int(self.port.get())
        try:
            # tcp连接
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = client
            # 若抓取到异常则在显示栏显示
            client.connect((dest_ip, dest_port))
            self.state.set("Connected")
            # 连接建立则关闭上一个窗口，即connection窗口
            f.destroy()
            # 新建一个新窗口
            # 登录或者注册的界面
            self.Signinorup_interface()
        except OSError:
            self.state.set("OSError")
        except ConnectionRefusedError:
            self.state.set("ConnectionRefuseError")
        except:
            self.state.set("Error")

    def start(self):
        # 连接的界面
        self.Connect_interface()
    # 用来接收服务器广播的消息
    def receive(self):
        while True:
            try:
                data = str(self.socket.recv(1024), encoding="utf-8")
                print(data)
                # 在界面打印消息包括别人和自己的
                self.message_list.insert(END, data)
            except ConnectionResetError:
                self.message_list.insert(END, "ConnectionResetError")
                break
            except:
                self.message_list.insert(END, "ConnectionResetError")
                break
        print("thread ends here")

    def send(self, event):
        data = self.entry.get()
        try:
            self.socket.send(bytes(data, encoding="utf-8"))
        except ConnectionResetError:
            self.message_list.insert(END, "ConnectionResetError")
            return
        except:
            self.message_list.insert(END, "Error")
            return
        # 每按下一次enter，将chatroom界面你的输入窗口清空
        self.v.set("")

    def Signinorup(self, method, f):
        # 从输入界面获取用户名及密码
        self.username = self.input_username.get()
        self.passward = self.input_passward.get()
        # 若用户名和密码均不为空，就做一下处理
        if self.username != "" and self.passward != "":
            # 发送给服务器的数据的格式
            data = method + ":" + self.username + ":" + self.passward
            try:
                self.socket.send(bytes(data, encoding="utf-8"))
            except ConnectionResetError:
                self.message_receive.set("ConnectionResetError")
                print("ConnectionResetError")
                return
            except:
                self.message_receive.set("Error")
                return

            try:
                message_recv = str(self.socket.recv(1024), encoding="utf-8")
            except OSError:
                self.message_receive.set("OSError")
                return
            except:
                self.message_receive.set("Error")
                return
            print(message_recv)
            # 用户名密码均正确，连接也一切正常
            if message_recv == "welcome":
                # 关闭登录或注册界面
                f.destroy()
                # 打开聊天界面
                self.chatroom_interface()
            else:
                self.message_receive.set(message_recv + "\n" + " Please sign in or up")
        elif self.username == "":
            self.message_receive.set("Username can't be empty, Please sign in or up")
        elif self.passward == "":
            self.message_receive.set("Passward can't be empty, Please sign in or up")

    def chatroom_interface(self):
        root = Tk()
        root.resizable(width=False, height=False)
        self.v = StringVar()
        # 界面右侧的滚动条
        scrollbar = Scrollbar(root)
        scrollbar.grid(row=0, column=2, sticky='ns')
        # 消息列表
        self.message_list = Listbox(root, font=("宋体", 20), yscrollcommand=scrollbar.set)
        self.message_list.grid(row=0, column=0, sticky='ew', columnspan=2)
        # 调用一个线程处理服务器广播的数据
        t1 = Thread(target=self.receive)
        # 将当前进程设置为守护进程，这样当聊天界面人为或意外关闭时，能将上面那个线程结束掉
        t1.setDaemon(True)
        t1.start()
        # 用来输入文字的控件
        self.entry = Entry(root, textvariable=self.v, font=('宋体', 20))
        self.entry.grid(row=4, column=0, sticky='wesn')
        enter = Button(root, text="enter", font=("宋体", 20), command=lambda: self.send(event="<Button-1>"))
        # 既可以通过点击按钮发送消息，也可以通过按回车发送消息
        self.entry.bind("<Return>", self.send)
        enter.grid(row=4, column=1)
        scrollbar.config(command=self.message_list.yview)
        root.mainloop()

    # 登录或注册的界面
    def Signinorup_interface(self):
        root = Tk()
        root.resizable(width=False, height=False)
        self.message_receive = StringVar()
        self.input_username = StringVar()
        self.input_passward = StringVar()
        self.message_receive.set("Please sign in or up")
        Label(root, text="MessageReceive:").grid(row=0, column=0)
        Label(root, textvariable=self.message_receive).grid(row=0, column=1)
        Label(root, text="Username", font=('宋体', 20)).grid(row=2, column=0)
        entry_name = Entry(root, textvariable=self.input_username, font=('宋体', 20))
        entry_name.grid(row=2, column=1, columnspan=3)
        Label(root, text="Passward", font=('宋体', 20)).grid(row=3, column=0)
        entry_pass = Entry(root, textvariable=self.input_passward, font=('宋体', 20))
        entry_pass.grid(row=3, column=1, columnspan=3)
        Button(root, text="Sign in", font=('宋体', 20), command=lambda: self.Signinorup(method="signin", f=root)).grid(row=4, column=1)
        Button(root, text="Sign up", font=('宋体', 20), command=lambda: self.Signinorup(method="signup", f=root)).grid(row=4, column=3)

        root.mainloop()
    # 建立连接的界面
    def Connect_interface(self):
        root = Tk()
        root.resizable(width=False, height=False)
        self.ip = StringVar()
        self.port = StringVar()
        self.state = StringVar()
        Label(text="Destination IP:").grid(row=0, column=0)
        entry_ip = Entry(root, textvariable=self.ip, font=('宋体', 20))
        entry_ip.grid(row=0, column=1, columnspan=3)
        Label(text="Destination Port:").grid(row=1, column=0)
        entry_port = Entry(root, textvariable=self.port, font=('宋体', 20))
        entry_port.grid(row=1, column=1, columnspan=3)
        Label(text="State:").grid(row=2,column=0)
        Label(textvariable=self.state).grid(row=2, column=1)
        Button(root, text="Connect", command=lambda: self.Connection(f=root)).grid(row=3, column=1, columnspan=2)
        root.mainloop()

# 程序入口
if __name__ == '__main__':
    chatroom = Chatroom()
    chatroom.start()
