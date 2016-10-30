#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-17
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/
import os
from module import actions
from module import db_handler
from conf import settings


ATM_AUTH_DIR = settings.DATABASE["path"]
ATM_CARD_LIST=os.listdir(ATM_AUTH_DIR)
atm_auth_flag = False
atm_auth_admin = False
atm_auth_card_id = ""

def atm_auth_log(atm_log):
    def atm_auth(func):
        def wrapper(*args, **kwargs):
            global ATM_CARD_LIST,atm_auth_flag, atm_auth_admin, atm_auth_card_id
            if atm_auth_flag:
                return func(*args, **kwargs)
            else:
                print("欢迎登陆华夏银行".center(50, "*"))
                auth_count = 0
                auth_id = ""
                while auth_count < 3:
                    auth_id = input("请输入卡号:").strip()
                    auth_passwd = input("请输入密码:").strip()
                    atm_log.info("Card:%s try %s login!"%(auth_id,auth_count+1))
                    if auth_id in ATM_CARD_LIST and actions.encry_passwd(auth_passwd) == db_handler.read_data(auth_id)["password"]:
                        auth_user_data=db_handler.read_data(auth_id)
                        atm_log.info("Card:%s login auth successful!"%auth_id)
                        if auth_user_data["freeze"]:
                            print("抱歉，您的信用卡:%s已被冻结，请联系管理人员解除冻结..." % auth_id)
                            atm_log.warning("Card:%s is freezed!login fail"%auth_id)
                            break
                        elif auth_user_data["privilege"] == "admin":
                            atm_auth_flag = True
                            atm_auth_admin = True
                            atm_auth_card_id = auth_user_data["card_id"]
                            atm_log.info("Card:%s is administrator!"%auth_id)
                            return func(*args, **kwargs)
                            break
                        else:
                            atm_auth_flag = True
                            atm_auth_card_id = auth_user_data["card_id"]
                            atm_log.info("Card:%s is user!"%auth_id)
                            return func(*args, **kwargs)
                            break
                    else:
                        print("抱歉，您输入的用户名或密码错误，请重新输入...")
                        atm_log.warning("Card:%s try %s login failed!"%(auth_id,auth_count+1))
                        auth_count += 1
                else:
                    print("抱歉，您已连续三次输入错误,您的账户将会被冻结...")
                    if auth_id in ATM_CARD_LIST:
                        auth_user_data=db_handler.read_data(auth_id)
                        auth_user_data["freeze"] = True
                        db_handler.write_data(auth_id,auth_user_data)
                        atm_log.warning("Card:%s will be freeze!"%auth_id)

        return wrapper
    return atm_auth