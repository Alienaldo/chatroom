								高级聊天程序
一．	相关说明
1.	环境为python3.5，windows平台，ide为pycharm
2.	与实验报告相同目录下有三个文件夹：pycharm工程文件，py文件，打包的exe文件夹（使用了pyinstaller），除了名为py文件的文件夹外，剩下两个文件夹下均有两个文件夹，为server和client。打包exe文件中的server和client文件下均有相应的exe可执行文件，server.exe 和 client.exe。
二．	程序流程说明
1.	运行服务器程序（无界面）
2.	运行客户端程序（有界面），出现如下界面：
 
第二个栏为目标服务器的端口号(服务程序中默认的端口号是12345)，第三个栏为显示连接状态（在按下connect才会有相应显示,）。第一个栏为目标服务器的ip地址，这里需要作更多的说明，服务器程序中的默认ip地址是127.0.0.1，这时要想连接上目标服务器，在可在ip地址栏输入的有两个127.0.0.1，和localhost（不区分大小写），前者不需过多解释，后者计算机会在host文件中查找与该域名对应的ip地址即127.0.0.1，所以这两者可达到相同效果。
	3．若成功连接上服务器，则进入登录和注册界面，同时关闭上一个界面，新界面如下：
		 
服务器中默认注册的用户是，用户名： John，密码：12345， 没注册的用户需要先注册再登录，若用户名密码为空，登录时用户不存在于服务器内，用户存在于服务器但密码错误，注册时用户名已被已有用户占用，这时均会在messagereceive中显示相关报错
	4．若用户成功登入，则会进入聊天界面，同时关闭上一个界面，新界面如下：
		 
		每当有用户进入聊天室，服务器就会向此时在聊天室中的所有成员广播消息”welcome xxx”，用户在输入框输入消息后按下界面上的“enter”或者按下键盘的回车键均可向服务器发送消息，界面最右侧有一个滑轮可允许用户上下翻看消息，用户离开时也会在聊天室广播”xxx is gone”。
5．相关示例如下：
   
三．	代码说明
首先说明client.py文件
主要有一个类和main函数组成，如下图：
 
Chatroom.start()用来调用对象的方法connect_interface()
方法connect_interface用来生成连接的界面：
 
在该界面按下connect按键则会调用方法connection()，这个方法用来与服务器建立socket连接以及处理相关异常如下图：
 
若成果连接上目标服务器，则会调用下一个对象方法signinorup_interface，这个方法用来生成登录或注册界面，如下图：
 
按下signin或signup按键则会调用同一个方法signinorup用来处理登录和注测，如下图：
  
正确登入后则会调用方法
Chatroom_interface()用来产生聊天界面，方法内生成一个线程用来专门接收从服务器接收到的消息，按下消息窗口的enter键或按下键盘上的回车键则会将消息发送出去，如下图：
 

下面开始介绍server.py文件：
	代码主要由一个类，一个函数和main函数组成，如下图：
	 
Main函数调用server()函数来做准备与客户端建立连接，如下图：
 
下面开始介绍类chatroom()，它拥有两个类变量socket_list和user_info，前者存放客户端的套接字，后者用字典存放用户的注册信息，方法start调用signinorup方法来处理用户的登录或注册，如图：
	 
	若用户信息正确则调用方法chat()让用户进入聊天室，如下：
	 
在chat()方法中，接收从每个客户端发送来的信息并广播出去。
