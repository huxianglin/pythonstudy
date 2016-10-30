#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-08
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import json

login_status = False


def login_auth(auth_type="JD"):
    def login_require(func):
        def wrapper(*args, **kwargs):
            global login_status
            if login_status:
                func(*args, **kwargs)
            else:
                print("欢迎来到京东购物平台，请先登录".center(50, "*"))
                auth_num = 0
                while True:
                    if auth_num == 3:
                        print("抱歉，您已连续输入错误三次账号密码，认证失败...")
                        break
                    elif auth_type == "JD":
                        data = read_auth_file("JD_auth.txt")
                        username = input("请输入京东账户用户名:")
                        password = input("请输入京东账户密码:")
                        if [True for i in data if username == i["username"] and password == i["password"]]:
                            login_status = True
                            func(*args, **kwargs)
                            break
                        else:
                            auth_num += 1
                            print("抱歉，您输入的账户名和密码错误，您还有%s次输入机会..." % (3 - auth_num))
                            continue
                    elif auth_type == "weixin":
                        data = read_auth_file("weixin_auth.txt")
                        username = input("请输入微信账户用户名:")
                        password = input("请输入微信账户密码:")
                        if [True for i in data if username == i["username"] and password == i["password"]]:
                            login_status = True
                            func(*args, **kwargs)
                            break
                        else:
                            auth_num += 1
                            print("抱歉，您输入的账户名和密码错误，您还有%s次输入机会..." % (3 - auth_num))
                            continue

        return wrapper

    return login_require


@login_auth()
def home(name):
    print("welcome to %s page" % name)


@login_auth("weixin")
def finance(name):
    print("welcome to %s page" % name)


@login_auth()
def book(name):
    print("welcome to %s page" % name)


def read_auth_file(file_name):
    return json.load(open(file_name, "r", encoding="utf-8"))


def write_auth_file(data, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f)


def main():
    # data=[{"username":"huxianglin","password":"123456"},{"username":"alex","password":"abcde"},{"username":"alvin","password":"qwerty"}]
    # write_auth_file(data,"JD_auth.txt")
    # write_auth_file(data,"weixin_auth.txt")
    page_list = ["home", "finance", "book"]
    while True:
        print("欢迎来到京东购物平台".center(50, "*"))
        for i, j in enumerate(page_list, 1):
            print("%s:%s" % (i, j))
        page_num = input("请输入想进入页面的编号:").strip()
        if page_num.isdigit():
            page_num = int(page_num)
            if page_num == 1:
                home("home")
            elif page_num == 2:
                finance("finance")
            elif page_num == 3:
                book("book")
            else:
                print("抱歉，您输入的编号不在页面列表中...")
        else:
            print("请输入正确的内容...")


if __name__ == "__main__":
    main()
