#!/usr/bin/env python
# encoding:utf-8
# __author__: client
# date: 2016/10/2 14:16
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/
import os
import uuid
import json
import sys
import queue
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import settings
from public import commons


class Client:
    def __init__(self, username, passwd, space_quota, privilege, uid=False):
        self.username = username
        self.passwd = commons.encrypt_passwd(passwd)
        self.uid = uid if uid else str(uuid.uuid1())
        self.home = os.path.join(settings.CLI_HOME_DIR, self.uid)
        self.current_dir = self.home
        self.space_quota = space_quota  # 磁盘空间大小
        self.privilege = privilege
        self.oper_sys = "linux" if "posix" in sys.builtin_module_names else "win"
        if not os.path.isdir(self.home):
            self.create_home()

    def create_home(self):
        """创建家目录"""
        try:
            os.mkdir(self.home)
        except Exception as e:
            print(e)

    @staticmethod
    def auth_user(user_info):
        """认证
        :param user_info: first param
        """
        user_name, passwd = user_info.split("|")
        for i in os.listdir(settings.CLI_DATA_DIR):
            cli_obj = json.load(open(os.path.join(settings.CLI_DATA_DIR, i)))
            if user_name == cli_obj["username"] and commons.encrypt_passwd(passwd) == cli_obj["passwd"]:
                return Client(cli_obj["username"], cli_obj["passwd"], cli_obj["space_quota"], cli_obj["privilege"],
                              cli_obj["uuid"])
        else:
            return None

    def upload(self, conn, cli_addr, operation):
        """上传文件 operation:upload,filename,filesize
        :param conn: first param
        :param cli_addr: second param
        :param operation: third param
        """
        file_size = int(operation[2])  # 获取文件大小
        space, usage_space, usage_percent = self.check_space()
        if usage_space + file_size > space:  # 判断空间使用超标，则返回错误
            conn.sendall(bytes("outofsize", "utf8"))  # check_data
            return None

        """对远端路径进行操作"""
        if operation[3] == "none":  # 未标示远程路径
            file_path = os.path.join(self.current_dir, operation[1])  # 获取文件绝对路径
        else:  # 标示远程路径
            if self.oper_sys == "win":  # 判断操作系统
                operation[3] = operation[3].replace("/", "\\")
            file_dir = os.path.join(self.current_dir, operation[3])  # 获取远端的文件父目录
            if not os.path.isdir(file_dir):  # 判断发送的远程路径不存在，则创建远程路径
                os.makedirs(file_dir)
            file_path = os.path.join(file_dir, operation[1])  # 获取文件绝对路径

        if os.path.exists(file_path):  # 判断文件是否存在，如果存在，求hash值，如果一致就不传输，否则，判断文件大小，实现断点续传
            get_hash = commons.get_file_hash(file_path)
            conn.sendall(bytes("|".join(("ok", get_hash)), "utf8"))  # check_data
            get_flag = str(conn.recv(1024), "utf8")  # 获取客户端发过来的hash比对结果
            if get_flag == "ok":  # 比对结果一致，则不上传文件
                return None
            else:  # 文件hash值不一样时
                local_file_size = os.stat(file_path).st_size
                conn.sendall(bytes(str(local_file_size), "utf8"))  # 获取文件大小并发给客户端
                remain_file_size = int(str(conn.recv(1024), "utf8"))  # 接受剩下的文件大小
                conn.sendall(bytes("ok", "utf8"))  # 没有作用，用来防止传输黏连
                recv_size = 0
                print("client:%s port:%s start upload file %s"%(cli_addr[0],cli_addr[1],operation[1]))
                send_que=queue.LifoQueue()
                progress_line=threading.Thread(target=commons.show_progress_line,args=(send_que,remain_file_size))
                progress_line.daemon=True
                progress_line.start()
                try:
                    with open(file_path, "ab") as f:
                        while recv_size != remain_file_size:
                            data = conn.recv(1024)
                            f.write(data)
                            send_que.put(recv_size)
                            recv_size += len(data)
                        else:
                            send_que.put(recv_size)
                            conn.sendall(bytes("true", "utf8"))
                except Exception as e:
                    print(e)
                    conn.sendall(bytes("false", "utf8"))
        else:  # 文件不存在时
            conn.sendall(bytes("|".join(("ok", "none")), "utf8"))  # check_data
            recv_size = 0
            print("client:%s port:%s start upload file %s"%(cli_addr[0],cli_addr[1],operation[1]))
            send_que=queue.LifoQueue()
            progress_line=threading.Thread(target=commons.show_progress_line,args=(send_que,file_size))
            progress_line.daemon=True
            progress_line.start()
            try:
                with open(file_path, "wb") as f:
                    while recv_size != file_size:
                        data = conn.recv(1024)
                        f.write(data)
                        send_que.put(recv_size)
                        recv_size += len(data)
                    else:
                        send_que.put(recv_size)
                        conn.sendall(bytes("true", "utf8"))
            except Exception as e:
                print(e)
                conn.sendall(bytes("false", "utf8"))

    def download(self, conn, cli_addr, operation):
        """下载文件
        :param conn: first param
        :param cli_addr: first param
        :param operation: second param
        """
        init_file_path = operation[1]  # 获取用户输入文件路径
        if self.oper_sys == "win":  # 如果是windows则将路径转换
            init_file_path = init_file_path.replace("/", "\\")
        filename=os.path.basename(init_file_path)  # 获取文件名
        file_path = os.path.join(self.current_dir, init_file_path)  # 获取文件路径
        if os.path.isfile(file_path):  # 文件存在
            file_size = os.stat(file_path).st_size  # 获取到文件大小
            get_hash=commons.get_file_hash(file_path)  #获取到文件hash值
            conn.sendall(bytes("|".join(("ok",filename,str(file_size),get_hash)), "utf8"))
            check_data=str(conn.recv(1024),"utf8")
            if check_data=="ok":  # 客户端有该文件
                return None
            elif check_data=="none":  # 客户端不存在该文件
                send_size=0
                print("client:%s port:%s start download file %s"%(cli_addr[0],cli_addr[1],filename))
                send_que=queue.LifoQueue()
                progress_line=threading.Thread(target=commons.show_progress_line,args=(send_que,file_size))
                progress_line.daemon=True
                progress_line.start()
                with open(file_path, "rb") as f:
                    while send_size!=file_size:
                        data = f.read(1024)
                        conn.send(data)
                        send_que.put(send_size)
                        send_size += len(data)
                    else:
                        send_que.put(send_size)
                final_check=str(conn.recv(1024),"utf8")
                if not final_check == "true":
                    print("client:%s port:%s download file %s failed!"%(cli_addr[0],cli_addr[1],filename))
            else:  # 客户端存在该文件
                send_size=int(check_data)
                print("client:%s port:%s start download file %s"%(cli_addr[0],cli_addr[1],filename))
                send_que=queue.LifoQueue()
                progress_line=threading.Thread(target=commons.show_progress_line,args=(send_que,file_size))
                progress_line.daemon=True
                progress_line.start()
                with open(file_path, "rb") as f:
                    f.seek(send_size)
                    while send_size!=file_size:
                        data = f.read(1024)
                        conn.send(data)
                        send_que.put(send_size)
                        send_size+=len(data)
                    else:
                        send_que.put(send_size)
                final_check=str(conn.recv(1024),"utf8")
                if not final_check=="true":
                    print("client:%s port:%s download file %s failed!"%(cli_addr[0],cli_addr[1],filename))
        else:  # 文件不存在
            conn.sendall(bytes("none|none", "utf8"))

    def remove(self, conn, cli_addr, operation):
        """删除文件
        :param conn: first param
        :param cli_addr: first param
        :param operation: second param
        """
        rm_dir = operation[1] if len(operation) >= 2 else None
        if rm_dir:
            rm_dir = os.path.join(self.current_dir, rm_dir.rstrip("/"))
            if os.path.isdir(rm_dir):  # 删除的如果是目录，则需要遍历取出其下的所有文件名和目录名，并且目录名得使用栈保存
                print("client:%s port:%s start del dir %s"%(cli_addr[0],cli_addr[1],rm_dir))
                dir_list = queue.Queue()  # 存储需要遍历的目录及子目录
                file_list = queue.Queue()  # 存储遍历出来的文件
                rm_dir_list = queue.LifoQueue()  # 存储遍历出来的目录及子目录，必须使用栈存储，如果使用队列，在删除的时候将会导致从父目录开始删除
                dir_list.put(rm_dir)
                while not dir_list.empty():  # 遍历目录
                    dir_name = dir_list.get()
                    rm_dir_list.put(dir_name)  # 将取出的目录压栈
                    for i in os.listdir(dir_name):  # 遍历目录下的文件及子目录
                        if os.path.isdir(os.path.join(dir_name, i)):
                            dir_list.put(os.path.join(dir_name, i))  # 将遍历的目录推到队列中
                        else:
                            file_list.put(os.path.join(dir_name, i))  # 将遍历的文件推到队列中

                while not file_list.empty():  # 遍历删除文件，文件需要先删除，否则目录无法删除
                    os.remove(file_list.get())
                while not rm_dir_list.empty():  # 遍历删除目录，采用出栈的方式删除，这样能保证每次拿到的目录都是最深的空目录
                    os.rmdir(rm_dir_list.get())
                conn.sendall(bytes("ok", "utf8"))
                print("client:%s port:%s del dir %s successful!"%(cli_addr[0],cli_addr[1],rm_dir))
            elif os.path.isfile(rm_dir):
                print("client:%s port:%s start del file %s"%(cli_addr[0],cli_addr[1],rm_dir))
                os.remove(rm_dir)
                conn.sendall(bytes("ok", "utf8"))
                print("client:%s port:%s del file %s successful!"%(cli_addr[0],cli_addr[1],rm_dir))
            else:
                conn.sendall(bytes("notdir", "utf8"))
        else:
            conn.sendall(bytes("error", "utf8"))

    def ls(self, conn, cli_addr, operation):
        """列出文件
        :param conn: first param
        :param cli_addr: first param
        :param operation: second param
        """
        list_dir = operation[1] if len(operation) >= 2 else None
        if list_dir:
            if list_dir == ".." or list_dir == "../":
                if self.current_dir != self.home:  # 上层目录没有超出家目录
                    list_dir = os.path.dirname(self.current_dir)
                    list_file = os.listdir(list_dir)
                    list_file = "\t".join(list_file)
                    self.send_data(conn, list_file)
                else:
                    conn.sendall(bytes("outhome", "utf8"))
            else:
                list_dir = list_dir.rstrip("/")
                if self.oper_sys == "win":  # 分操作系统
                    list_dir = list_dir.replace("/", "\\")
                list_dir = os.path.join(self.current_dir, list_dir)
                if os.path.isdir(list_dir):
                    list_file = os.listdir(list_dir)
                    list_file = "\t".join(list_file)
                    self.send_data(conn, list_file)
                else:
                    conn.sendall(bytes("notdir", "utf8"))
        else:
            list_file = os.listdir(self.current_dir)
            list_file = "\t".join(list_file)
            self.send_data(conn, list_file)

    def cd(self, conn, cli_addr, operation):
        """跳转目录
        :param conn: first param
        :param cli_addr: first param
        :param operation: second param
        """
        change_dir = operation[1] if len(operation) >= 2 else None
        if change_dir:
            if change_dir == ".." or change_dir == "../":
                if self.current_dir != self.home:
                    self.current_dir = os.path.dirname(self.current_dir)
                    conn.sendall(bytes("ok", "utf8"))
                else:
                    conn.sendall(bytes("outhome", "utf8"))
            else:
                change_dir = change_dir.rstrip("/")
                if self.oper_sys == "win":
                    change_dir = change_dir.replace("/", "\\")
                change_dir = os.path.join(self.current_dir, change_dir)
                if os.path.isdir(change_dir):
                    self.current_dir = change_dir
                    conn.sendall(bytes("ok", "utf8"))
                else:
                    conn.sendall(bytes("notdir", "utf8"))
        else:
            conn.sendall(bytes("error", "utf8"))

    def mkdir(self, conn, cli_addr, operation):
        """创建目录
        :param conn: first param
        :param cli_addr: first param
        :param operation: second param
        """
        mkdir = operation[1] if len(operation) >= 2 else None
        if mkdir:
            mkdir = os.path.join(self.current_dir, mkdir.rstrip("/"))
            os.makedirs(mkdir, exist_ok=True)
            conn.sendall(bytes("ok", "utf8"))
        else:
            conn.sendall(bytes("error", "utf8"))

    def check_space(self):
        """检查空间使用"""
        space = self.space_quota
        usage_space = 0
        dir_list = queue.Queue()
        dir_list.put(self.home)
        while not dir_list.empty():  # 循环遍历目录获取该目录下所有文件和目录大小
            dir_name = dir_list.get()
            for i in os.listdir(dir_name):
                usage_space += os.stat(os.path.join(dir_name, i)).st_size
                if os.path.isdir(os.path.join(dir_name, i)):
                    dir_list.put(os.path.join(dir_name, i))
        if "G" in space or "g" in space:
            space = int(space.split("G")[0].split("g")[0]) * 1024 ** 3
            usage_percent = "".join((str(usage_space * 100 // space), "%"))
        elif "M" in space or "m" in space:
            space = int(space.split("M")[0].split("m")[0]) * 1024 ** 2
            usage_percent = "".join((str(usage_space * 100 // space), "%"))
        elif "K" in space or "k" in space:
            space = int(space.split("K")[0].split("k")[0]) * 1024
            usage_percent = "".join((str(usage_space * 100 // space), "%"))
        return space, usage_space, usage_percent

    def info(self, conn, cli_addr, operation):
        """返回空间使用情况
        :param conn: first param
        :param cli_addr: first param
        :param operation: second param
        """
        space, usage_space, usage_percent = self.check_space()
        conn.sendall(bytes("|".join(("ok", str(space // (1024 ** 2)), str(usage_space // (1024 ** 2)), usage_percent)), "utf8"))

    def send_data(self, conn, data):
        """发送数据
        :param conn: first param
        :param data: second param
        """
        data_size = len(bytes(data, "utf8"))
        conn.sendall(bytes(str(data_size), "utf8"))
        conn.recv(1024)
        conn.sendall(bytes(data, "utf8"))

    def save_user(self):
        try:
            user_data = {"username": self.username, "passwd": self.passwd, "space_quota": self.space_quota,
                         "privilege": self.privilege, "uuid": self.uid}
            json.dump(user_data, open(os.path.join(settings.CLI_DATA_DIR, self.uid), "w"))
        except Exception as e:
            print(e)

    def __str__(self):
        """返回用户名"""
        return self.username

# huxianglin=Client("huxianglin","huxianglin","1024G","admin")
# huxianglin.save_user()
