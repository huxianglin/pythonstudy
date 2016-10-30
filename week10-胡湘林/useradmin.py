#!/usr/bin/env python
# encoding:utf-8
# __author__: useradmin
# date: 2016/10/30 12:49
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import pymysql
from queue import Queue

MYSQL_INFO = {"host": "192.168.12.120",
              "port": 3306,
              "user": "root",
              "passwd": "012615",
              "db": "useradmin",
              "charset": "utf8"
              }
USER_INFO = {}


class Exec_db:
    """对数据库进行抽象封装，使用单例模式，以及连接池实现，"""
    __v = None

    def __init__(self, host=None, port=None, user=None, passwd=None, db=None, charset=None, maxconn=5):
        self.host, self.port, self.user, self.passwd, self.db, self.charset = host, port, user, passwd, db, charset
        self.maxconn = maxconn
        self.pool = Queue(maxconn)
        for i in range(maxconn):
            try:
                conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                       charset=self.charset)
                conn.autocommit(True)
                # self.cursor=self.conn.cursor(cursor=pymysql.cursors.DictCursor)
                self.pool.put(conn)
            except Exception as e:
                raise IOError(e)

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls.__v:
            return cls.__v
        else:
            cls.__v = Exec_db(*args, **kwargs)
            return cls.__v

    def exec_sql(self, sql, operation=None):
        """
            执行无返回结果集的sql，主要有insert update delete
        """
        try:
            conn = self.pool.get()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            response = cursor.execute(sql, operation) if operation else cursor.execute(sql)
            newid = cursor.lastrowid
        except Exception as e:
            print(e)
            cursor.close()
            self.pool.put(conn)
            return None
        else:
            cursor.close()
            self.pool.put(conn)
            return response, newid

    def exec_sql_feach(self, sql, operation=None):
        """
            执行有返回结果集的sql,主要是select
        """
        try:
            conn = self.pool.get()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            response = cursor.execute(sql, operation) if operation else cursor.execute(sql)
        except Exception as e:
            print(e)
            cursor.close()
            self.pool.put(conn)
            return None, None
        else:
            data = cursor.fetchall()
            cursor.close()
            self.pool.put(conn)
            return response, data

    def exec_sql_many(self, sql, operation=None):
        """
            执行多个sql，主要是insert into 多条数据的时候
        """
        try:
            conn = self.pool.get()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            response = cursor.executemany(sql, operation) if operation else cursor.executemany(sql)
            newid = cursor.lastrowid
        except Exception as e:
            print(e)
            cursor.close()
            self.pool.put(conn)
        else:
            cursor.close()
            self.pool.put(conn)
            return response, newid

    def close_conn(self):
        for i in range(self.maxconn):
            self.pool.get().close()


obj = Exec_db.get_instance(host=MYSQL_INFO["host"], port=MYSQL_INFO["port"], user=MYSQL_INFO["user"],
              passwd=MYSQL_INFO["passwd"], db=MYSQL_INFO["db"], charset=MYSQL_INFO["charset"], maxconn=1)


class useroperation:
    def __init__(self, obj):
        self.obj = obj

    def show_local(self):
        user_info_dict = {"username": "用户名:", "email": "邮  箱:", "pname": "权限名:", "plist": "权  限:"}
        for i in USER_INFO:
            print(user_info_dict[i], USER_INFO[i])

    def show_all(self):
        sql = "select userinfo.username,userinfo.email,privileges.pname,privileges.plist from " \
              "userinfo left join privileges on userinfo.privilege_id=privileges.pid;"
        rst = self.obj.exec_sql_feach(sql)
        print("用户名\t\t邮箱\t\t\t权限名\t权限")
        for i in rst[1]:
            print(i["username"], i["email"], i["pname"], i["plist"])

    def update_user(self):
        print("请输入您要修改权限的用户名")
        username = input(">>>").strip()
        print("""请选择您要修改的权限
        1.普通用户
        2.管理员
        """)
        privilege = input(">>>").strip()
        sql = "select uid from userinfo where username=%s"
        rst = self.obj.exec_sql_feach(sql, username)
        if rst[0]:
            uid = rst[1][0]["uid"]
            if privilege.isdigit():
                privilege = int(privilege)
                if privilege in [1, 2]:
                    sql = "update userinfo set privilege_id=%s where uid=%s"
                    data = (privilege, uid)
                    rst = self.obj.exec_sql(sql, data)
                    if rst:
                        print("权限修改成功")
                    else:
                        print("内部错误...")
                else:
                    print("权限输入错误...")
            else:
                print("权限输入错误...")
        else:
            print("抱歉，用户%s不存在" % username)

    def exit(self):
        self.obj.close_conn()

    @staticmethod
    def auth_user(username, password):
        sql = "select uid from userinfo where username=%s and pwd=password(%s)"
        data = (username, password)
        rst = obj.exec_sql_feach(sql, data)
        if rst[0]:
            global USER_INFO
            sql = "select userinfo.username,userinfo.email,privileges.pname,privileges.plist from " \
                  "userinfo left join privileges on userinfo.privilege_id=privileges.pid where uid=%s;"
            data = rst[1][0]["uid"]
            rst = obj.exec_sql_feach(sql, data)
            USER_INFO = rst[1][0]
            return True
        else:
            return False

    @staticmethod
    def register_user(username, password, email):
        sql = "insert into userinfo(username,pwd,email,privilege_id) values(%s,password(%s),%s,1)"
        data = (username, password, email)
        rst = obj.exec_sql(sql, data)
        if rst[0] == 1:
            global USER_INFO
            sql = "select userinfo.username,userinfo.email,privileges.pname,privileges.plist from " \
                  "userinfo left join privileges on userinfo.privilege_id=privileges.pid where uid=%s;"
            data = rst[1]
            rst = obj.exec_sql_feach(sql, data)
            USER_INFO = rst[1][0]
            return True
        else:
            return False

    @staticmethod
    def change_password(username, email):
        sql = "select uid from userinfo where username=%s and email=%s"
        data = (username, email)
        rst = obj.exec_sql_feach(sql, data)
        if rst[0]:
            uid = rst[1][0]["uid"]
            new_password = input("请输入新密码>>>").strip()
            sql = "update userinfo set pwd=password(%s) where uid=%s"
            data = (new_password, uid)
            rst = obj.exec_sql(sql, data)
            if rst:
                global USER_INFO
                sql = "select userinfo.username,userinfo.email,privileges.pname,privileges.plist from " \
                      "userinfo left join privileges on userinfo.privilege_id=privileges.pid where uid=%s;"
                data = uid
                rst = obj.exec_sql_feach(sql, data)
                USER_INFO = rst[1][0]
                return True
            else:
                return False
        else:
            print("输入的信息错误...")
            return False


def register():
    print("""
    注册需要填写资料：
    1.用户名
    2.密码
    3.邮箱
    """)
    username = input("用户名:").strip()
    password = input("密  码:").strip()
    email = input("邮  箱:").strip()
    if username and password and email:
        rst = useroperation.register_user(username, password, email)
        if rst:
            print("恭喜，注册成功")
            return True
        else:
            print("内部错误。。。")
            return False
    else:
        print("输入有误,注册失败...")
        return False


def get_user():
    username = input("username:").strip()
    password = input("password:").strip()
    rst = useroperation.auth_user(username, password)
    return True if rst else False


def get_password():
    username = input("请输入用户名:").strip()
    email = input("请输入注册时邮箱:").strip()
    if username and email:
        rst = useroperation.change_password(username, email)
        if rst:
            print("密码修改成功")
            return True
        else:
            print("密码修改失败...")
            return False
    else:
        print("输入错误...")
        return False


def login(func):
    def wrapper(*args, **kwargs):
        while True:
            if not USER_INFO:
                init_oper = {"1": get_user, "2": register, "3": get_password}
                print("""******欢迎来到用户管理系统******
        1.登录
        2.注册
        3.找回密码
                """)
                choice = input(">>>").strip()
                if choice in init_oper:
                    rst = init_oper[choice]()
                    if rst:
                        return func(*args, **kwargs)
                    else:
                        continue
            else:
                return func(*args, **kwargs)

    return wrapper


@login
def main():
    oper_dict = {"show_local": "查看当前用户信息", "show_all": "查看所有用户信息", "update_user": "给用户授权", "exit": "退出"}
    user_oper_dict = dict(zip(range(1, len(USER_INFO["plist"]) + 1), USER_INFO["plist"].split(",")))
    user_oper_dict[len(user_oper_dict) + 1] = "exit"
    oper_obj = useroperation(obj)
    while True:
        for i in user_oper_dict:
            print(i, oper_dict[user_oper_dict[i]])
        operation = input(">>>").strip()
        if operation.isdigit():
            operation = int(operation)
            if operation not in user_oper_dict:
                print("输入有误...")
                continue
            else:
                getattr(oper_obj, user_oper_dict[operation])()
                if user_oper_dict[operation] == "exit":
                    break
        else:
            print("输入有误...")
            continue


if __name__ == "__main__":
    main()
