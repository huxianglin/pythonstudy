#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-18
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

from shop_conf import settings
from shop_module import encry_passwd
from shop_module import db_handler
import os

INIT_DATA={
    "shop_user_id":"",
    "shop_user_flag":False,
    "shop_user_admin":False,
    "shop_user_list":os.listdir(settings.USER_DATABASE["path"]),
    "shop_user_path":settings.USER_DATABASE["path"]
}

def shop_auth_log(shop_log):
    def shop_auth(func):
        def wrapper(*args,**kwargs):
            global INIT_DATA
            if INIT_DATA["shop_user_flag"]:
                func(*args, **kwargs)
            else:
                print("欢迎登陆华联超市".center(50, "*"))
                auth_count = 0
                auth_id = ""
                while auth_count < 3:
                    auth_id = input("请输入账号:").strip()
                    auth_passwd = input("请输入密码:").strip()
                    shop_log.info("ID:%s try %s login!"%(auth_id,auth_count+1))
                    if auth_id in INIT_DATA["shop_user_list"] and encry_passwd.encry_passwd(auth_passwd) == db_handler.read_user(auth_id)["password"]:
                        auth_user_data=db_handler.read_user(auth_id)
                        shop_log.info("ID:%s login auth successful!"%auth_id)
                        if auth_user_data["freeze"]:
                            print("抱歉，您的账号:%s已被冻结，请联系管理人员解除冻结..." % auth_id)
                            shop_log.warning("ID:%s is freezed!login failed!"%auth_id)
                            break
                        elif auth_user_data["privilege"] == "admin":
                            INIT_DATA["shop_user_flag"] = True
                            INIT_DATA["shop_user_admin"] = True
                            INIT_DATA["shop_user_id"] = auth_user_data["user_id"]
                            shop_log.info("ID:%s is administrator!"%auth_id)
                            func(*args, **kwargs)
                            break
                        else:
                            INIT_DATA["shop_user_flag"] = True
                            INIT_DATA["shop_user_id"] = auth_user_data["user_id"]
                            shop_log.info("ID:%s is user!"%auth_id)
                            func(*args, **kwargs)
                            break
                    else:
                        print("抱歉，您输入的用户名或密码错误，请重新输入...")
                        shop_log.warning("ID:%s try %s login failed!"%(auth_id,auth_count+1))
                        auth_count += 1
                else:
                    print("抱歉，您已连续三次输入错误,您的账户将会被冻结...")
                    if auth_id in INIT_DATA["shop_user_list"]:
                        auth_user_data=db_handler.read_user(auth_id)
                        auth_user_data["freeze"] = True
                        db_handler.write_user(auth_id,auth_user_data)
                        shop_log.warning("ID:%s will be freeze!"%auth_id)
        return wrapper
    return shop_auth