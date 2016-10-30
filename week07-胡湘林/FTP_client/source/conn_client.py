#!/usr/bin/env python
# encoding:utf-8
# __author__: conn_client
# date: 2016/10/2 16:01
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import socket
import os
import sys
import threading
import queue
import time
import getpass
from conf import settings
from public import commons

HOMEDIR=settings.HOMEDIR
OPER_SYS=settings.OPER_SYS
stat=True

def upload(sk,operation):
    """上传文件"""
    global HOMEDIR
    try:
        if OPER_SYS=="win":  # 判断操作系统
            operation[1]=operation[1].replace("/","\\")
        filedir=os.path.join(HOMEDIR,operation[1])  # 如果第二个参数不存在，这里会抛异常
    except Exception as e:
        print("语法错误...")
        return False
    if os.path.isfile(filedir):  # 本地文件存在
        filename=os.path.basename(filedir)  # 获取文件名
        filesize=os.stat(filedir).st_size  # 获取文件大小
        if len(operation)<3:  # 如果有第三个参数，则第三个参数是远程目录，否则远程目录是none
            distination_dir="none"
        else:
            distination_dir=operation[2]  # 远程目录
        sk.sendall(bytes("|".join((operation[0],filename,str(filesize),distination_dir)),"utf8"))  # 发送操作命令 文件名 文件大小 目的目录
        check_data=str(sk.recv(1024),"utf8")  # 接收服务器传输过来的判断结果，三种结果：空间超过限制 文件存在 文件不存在
        if check_data == "outofsize":  # 如果超过限制，结束
            print("空间已满...")
            return False
        check_data=check_data.split("|")  # 否则判断传过来的第二个参数是hash还是none

        if check_data[1]=="none":  # 文件不存在
            send_size=0
            print("Start upload file %s"%(filename))
            send_que=queue.LifoQueue()
            progress_line=threading.Thread(target=commons.show_progress_line,args=(send_que,filesize))
            progress_line.daemon=True
            progress_line.start()
            with open(filedir,"rb") as f:
                while send_size!=filesize:
                    data=f.read(1024)
                    sk.sendall(data)
                    send_que.put(send_size)
                    send_size+=len(data)
                else:
                    send_que.put(send_size)
            flag=str(sk.recv(1024),"utf8")
            time.sleep(settings.PROGRESS_LINE_PERIOD*2)
            return True if flag=="true" else False
        else:
            file_md5=commons.get_file_hash(filedir)  # 获取本地文件hash值
            if file_md5==check_data[1]:  # 文件hash值相同时，不传输文件，终止
                sk.sendall(bytes("ok","utf8"))
                print("远程文件和本地文件一致...")
                return False
            else:  # 文件存在但hash不一致
                sk.sendall(bytes("false","utf8"))  # 这个是为了让服务端接受到结果，没有作用
                remote_file_size=int(str(sk.recv(1024),"utf8"))  # 接受远程文件大小
                remain_file_size=os.stat(filedir).st_size-remote_file_size  # 本地文件减去远程文件大小
                sk.sendall(bytes(str(remain_file_size),"utf8"))  # 发送剩余文件大小
                sk.recv(1024)  # 没有作用，用来防止黏连
                send_size=remote_file_size
                print("Start upload file %s"%(filename))
                send_que=queue.LifoQueue()
                progress_line=threading.Thread(target=commons.show_progress_line,args=(send_que,filesize))
                progress_line.daemon=True
                progress_line.start()
                with open(filedir,"rb") as f:
                    f.seek(remote_file_size)  # 移动seek到指定位置
                    while send_size!=filesize:
                        data=f.read(1024)
                        sk.sendall(data)
                        send_que.put(send_size)
                        send_size+=len(data)
                    else:
                        send_size+=len(data)
                flag=str(sk.recv(1024),"utf8")
                time.sleep(settings.PROGRESS_LINE_PERIOD*2)
                return True if flag=="true" else False

    else:
        print("本地文件路径错误...")
        return False

def download(sk,operation):
    """下载文件"""
    global HOMEDIR
    if len(operation)>=2:  # 如果有两个以上参数才能达到最基本条件
        if len(operation)>=3:  # 有第三个参数的时候
            if OPER_SYS=="win":  # 判断操作系统
                operation[2]=operation[2].replace("/","\\")
            local_file_dir=os.path.join(HOMEDIR,operation[2])
        else:
            local_file_dir=HOMEDIR
    else:
        print("语法错误...")  # 少于两个参数，直接报错返回
        return  False
    os.makedirs(local_file_dir,exist_ok=True)  # 创建本地目录，如果本地目录存在，则不创建
    sk.sendall(bytes("|".join(operation),"utf8"))
    # filename=operation[1]
    chack_data=str(sk.recv(1024),"utf8").split("|")
    if chack_data[0]=="none":  # 文件在服务器上不存在
        print("服务端文件不存在...")
        return False
    else:  # 服务器上存在文件，这时分两种情况，一种客户端不存在文件，另一种客户端存在文件
        filename=chack_data[1]  # 获取文件名
        filesize=int(chack_data[2])  # 获取文件大小
        file_md5=chack_data[3]  # 获取文件hash值
        file_path=os.path.join(local_file_dir,filename)  # 生成文件在本地的存储路径
        if os.path.isfile(file_path):  # 如果本地存在文件，则分两种情况，一种是文件hash值一致，另一种是hash值不一致
            if file_md5 == commons.get_file_hash(file_path):  # 本地文件hash值和远端一致
                sk.sendall(bytes("ok","utf8"))
                print("本地文件和服务器一致...")
                return False
            else:  # 本地文件hash值和远端文件不一致
                local_file_size=os.stat(file_path).st_size
                sk.sendall(bytes(str(local_file_size),"utf8"))
                recv_size=local_file_size
                print("Start download file %s"%(filename))
                send_que=queue.LifoQueue()
                progress_line=threading.Thread(target=commons.show_progress_line,args=(send_que,filesize))
                progress_line.daemon=True
                progress_line.start()
                with open(file_path,"ab") as f:
                    while recv_size != filesize:
                        data=sk.recv(1024)
                        f.write(data)
                        send_que.put(recv_size)
                        recv_size+=len(data)
                    else:
                        send_que.put(recv_size)
                        sk.sendall(bytes("true","utf8"))
                time.sleep(settings.PROGRESS_LINE_PERIOD*2)
                return True

        else:  # 本地不存在文件
            sk.sendall(bytes("none","utf8"))
            recv_size=0
            print("Start download file %s"%(filename))
            send_que=queue.LifoQueue()
            progress_line=threading.Thread(target=commons.show_progress_line,args=(send_que,filesize))
            progress_line.daemon=True
            progress_line.start()
            with open(file_path,"wb") as f:
                while recv_size != filesize:
                    data=sk.recv(1024)
                    f.write(data)
                    send_que.put(recv_size)
                    recv_size+=len(data)
                else:
                    send_que.put(recv_size)
                    sk.sendall(bytes("true","utf8"))
            time.sleep(settings.PROGRESS_LINE_PERIOD*2)
            return True

def list_file(sk,operation):
    """展示目录"""
    sk.sendall(bytes("|".join(operation),"utf8"))
    data_size=str(sk.recv(1024),"utf8")
    if data_size == "outhome":
        print("跳出家目录了...")
        return False
    elif data_size == "notdir":
        print("目录不存在...")
        return False
    else:
        data_size=int(data_size)
        sk.send(bytes("ok","utf8"))
        recv_size=0
        data=bytes()
        while recv_size != data_size:
            recv_data=sk.recv(1024)
            data+=recv_data
            recv_size+=len(data)
        print(str(data,"utf8"))
        return True

def change_dir(sk,operation):
    sk.sendall(bytes("|".join(operation),"utf8"))
    data=str(sk.recv(1024),"utf8")
    if data == "ok":
        return True
    elif data=="outhome":
        print("超出家目录了...")
        return False
    elif data=="notdir":
        print("目录不存在...")
        return False

def mkdir(sk,operation):
    sk.sendall(bytes("|".join(operation),"utf8"))
    data=str(sk.recv(1024),"utf8")
    if data == "ok":
        return True
    else:
        return False

def remove(sk,operation):
    sk.sendall(bytes("|".join(operation),"utf8"))
    data=str(sk.recv(1024),"utf8")
    if data == "ok":
        return True
    else:
        return False

def info(sk,operation):
    sk.sendall(bytes("|".join(operation),"utf8"))
    data=str(sk.recv(1024),"utf8")
    if "ok" in data:
        data=data.split("|")
        print("space:%sM usage:%sM percent%s"%(data[1],data[2],data[3]))
        return True
    else:
        return False

def exit_client(sk,operation):
    print("Bye,Bye...")
    sk.close()
    global stat
    stat=False
    return True

def conn_server(operation=False):
    sk=socket.socket()
    sk.connect((settings.SERVER_IP,settings.SERVER_PORT))
    operations={"cd":change_dir,"ls":list_file,"upload":upload,"download":download,"remove":remove,
                                "mkdir":mkdir,"info":info,"exit":exit_client}

    global stat
    while stat:
        username=input("pls input username:").strip()
        if sys.stdin.isatty():  # 如果是tty终端，则正常调用getpass模块
            passwd=getpass.getpass(prompt="pls input passwd:")
        else:  # 否则，getpass模块无法使用
            print("Is not tty pls input passwd:",end="",flush=True)
            passwd = sys.stdin.readline().rstrip()
        # passwd=getpass.getpass(prompt="pls input passwd:")
        user_info="|".join((username,passwd))
        sk.sendall(bytes(user_info,"utf8"))
        flag=str(sk.recv(1024),"utf8")
        if flag == "false":
            print("username or passwd wrong...")
            continue
        elif flag == "true":
            if operation:
                flag=operations[operation[0]](sk,operation)
                print("operation is successful!") if flag else print("operation is invalid!")
                return None
            while stat:
                operation=input(">>>").strip().split()
                if operation != []:
                    if operation[0] in operations:
                        flag=operations[operation[0]](sk,operation)
                        print("operation is successful!") if flag else print("operation is invalid!")
                    else:
                        print("input error....")
                else:
                    continue

if __name__=="__main__":
    conn_server()


