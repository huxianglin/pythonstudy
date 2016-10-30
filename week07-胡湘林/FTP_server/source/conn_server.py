#!/usr/bin/env python
# encoding:utf-8
# __author__: conn_server
# date: 2016/10/2 14:17
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import socketserver
from conf import settings
from source.client_user import Client

class Myserver(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            while True:
                conn=self.request  # 客户端对象
                cli_addr=self.client_address  # 客户端地址
                user_info=str(conn.recv(1024),"utf8")  # 获取用户名密码
                cli_obj=Client.auth_user(user_info)  # 认证用户名密码
                if not cli_obj:  # 认证失败
                    conn.sendall(bytes("false","utf8"))
                    continue
                else:  # 认证成功
                    conn.sendall(bytes("true","utf8"))
                    while True:  # 循环接收客户操作
                        operation=list()  # 接收用户操作指令列表
                        operation_str=str(conn.recv(1024),"utf8")
                        try:
                            operation=operation_str.split("|")  # 用户可能传入异常操作，需要在这捕获异常
                        except Exception:
                            operation[0]=operation_str  # 如果操作只有一个字符串，则直接赋值给列表的第一个空间
                        # operations={"upload":cli_obj.upload_file,"download":cli_obj.download_file,"ls":cli_obj.list_file,  # 之前是使用字典实现的，后来改成反射实现
                        #             "cd":cli_obj.change_dir,"mkdir":cli_obj.creat_dir,"remove":cli_obj.remove_file,
                        #             "info":cli_obj.get_space}
                        # if operation[0] in operations:operations[operation[0]](conn,cli_addr,operation)
                        # print(cli_obj.__dict__)
                        # print(Client.__dict__)
                        if hasattr(cli_obj,operation[0]):  # 反射
                            getattr(cli_obj,operation[0])(conn,cli_addr,operation)
                        else:
                            continue
        except Exception as e:
            print(e)
            conn.close()

def main():
    server=socketserver.ThreadingTCPServer((settings.IPADDR,settings.PORT),Myserver)
    server.serve_forever()

if __name__=="__main__":
    main()