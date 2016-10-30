#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-17
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import os
from conf import settings
from module import actions
from module import db_handler
from module import auth

def admin(atm_log):  # 管理
    operations = {"添加":__add_user__, "删除":__del_user__, "修改":__mod_user__, "查询":__que_user__, "修改密码":__mod_passwd__, "解除冻结":__remove_freeze__}
    while True:
        operation_flag = actions.operations(operations,atm_log)
        if not operation_flag:
            break

def __add_user__(atm_log):
    while True:
        new_user_info = {"card_id":"","password": "", "privilege": "", "username": "", "balance": 0, "limit": 15000, "freeze": False}
        card_id = input("请输入6位用户卡号,b返回:").strip()
        if card_id == "b":
            break
        elif len(card_id) != 6 or not card_id.isdigit():
            print("抱歉，您输入的卡号有误...")
        elif card_id in auth.ATM_CARD_LIST:
            print("抱歉，您输入的卡号已存在...")
        else:
            new_user_info["card_id"]=card_id
            password = input("请输入密码:").strip()
            new_user_info["password"] = actions.encry_passwd(password)
            while True:
                privilege = input("请输入用户权限，user或admin:").strip()
                if privilege not in ["user", "admin"]:
                    print("抱歉，您输入的权限不合法....")
                else:
                    new_user_info["privilege"] = privilege
                    break
            new_user_info["username"] = input("请输入用户名:").strip()
            while True:
                remainder = input("请输入卡内初始余额:").strip()
                if remainder.isdigit():
                    new_user_info["remainder"] = int(remainder)
                    break
                else:
                    print("您输入的余额不合法...")
            while True:
                limit = input("请输入限额,默认1.5W,默认请回车:").strip()
                if limit:
                    if limit.isdigit():
                        new_user_info["limit"] = int(limit)
                        break
                    else:
                        print("抱歉，您的输入不合法...")
                else:
                    break
            atm_log.info("Add new card %s successful!"%new_user_info["card_id"])
            db_handler.write_data(card_id, new_user_info)
            auth.ATM_CARD_LIST=os.listdir(settings.DATABASE["path"])


def __del_user__(atm_log):
    while True:
        for i, j in enumerate(auth.ATM_CARD_LIST, 1):
            print(i, j)
        del_operation = input("请输入要删除的卡号,b返回:").strip()
        if del_operation == "b":
            break
        elif del_operation in auth.ATM_CARD_LIST:
            os.remove(os.path.join(settings.DATABASE["path"],del_operation))
            auth.ATM_CARD_LIST=os.listdir(settings.DATABASE["path"])
            atm_log.info("Del card %s successful!"%del_operation)
        else:
            print("抱歉，您的输入有误...")


def __mod_user__(atm_log):
    while True:
        for i, j in enumerate(auth.ATM_CARD_LIST, 1):
            print(i, j)
        mod_card_id = input("请输入要修改的卡号,b返回:").strip()
        if mod_card_id == "b":
            break
        elif mod_card_id in auth.ATM_CARD_LIST:
            mod_user_data=db_handler.read_data(mod_card_id)
            print("卡号:%s的信息如下:" % mod_card_id)
            print("密码:xxx 权限:%s 用户名:%s 余额:%s 额度:%s 冻结:%s" %
                  (mod_user_data["privilege"], mod_user_data["username"],
                   mod_user_data["balance"], mod_user_data["limit"],mod_user_data["freeze"]))
            mod_info_list = input("请按照如下选项进行修改，每项之间用空格分隔:\n密码 权限(user or admin) 用户名 "
                                  "余额 额度 冻结(true or false)\n>>>").strip().split()
            if len(mod_info_list) == 6 and mod_info_list[1] in ["user", "admin"] and mod_info_list[3].isdigit() and \
                    mod_info_list[4].isdigit() and mod_info_list[5] in ["true", "false"]:
                print("卡号:%s更新成功" % mod_card_id)
                mod_info_list[0] = actions.encry_passwd(mod_info_list[0])
                mod_info_list[3], mod_info_list[4],  = int(mod_info_list[3]), int(mod_info_list[4])
                if mod_info_list[5] == "true":
                    mod_info_list[5] = True
                else:
                    mod_info_list[5] = False
                mod_info_list.reverse()
                for i in ["password","privilege","username","balance","limit","freeze"]:
                    mod_user_data[i]=mod_info_list.pop()
                db_handler.write_data(mod_card_id, mod_user_data)
                atm_log.info("Modefy card %s successful!"%mod_user_data["card_id"])
            else:
                print("抱歉，您的输入不符合格式...")
        else:
            print("抱歉，您的输入有误...")


def __que_user__(atm_log):
    while True:
        for i, j in enumerate(auth.ATM_CARD_LIST, 1):
            print(i, j)
        queue_card_id = input("请输入要查询的卡号,b返回:").strip()
        if queue_card_id in auth.ATM_CARD_LIST:
            que_user_info=db_handler.read_data(queue_card_id)
            print("卡号:%s的信息如下:" % queue_card_id)
            print("密码:xxx 权限:%s 用户名:%s 余额:%s 额度:%s 冻结:%s" %
                  (que_user_info["privilege"], que_user_info["username"],
                   que_user_info["balance"], que_user_info["limit"], que_user_info["freeze"]))
            atm_log.info("Queue card %s successful!" % que_user_info["card_id"])
        elif queue_card_id == "b":
            break
        else:
            print("抱歉，请输入正确的卡号...")


def __mod_passwd__(atm_log):
    mod_card = input("请输入修改密码的卡号:")
    if mod_card in auth.ATM_CARD_LIST:
        mod_user_data=db_handler.read_data(mod_card)
        mod_password = input("请输入新密码:")
        mod_user_data["password"] = actions.encry_passwd(mod_password)
        db_handler.write_data(mod_card, mod_user_data)
        atm_log.info("Modefy card %s password successful!"%mod_user_data["card_id"])
    else:
        print("抱歉，您输入的卡号不在系统中...")


def __remove_freeze__(atm_log):
    remove_freeze_card = input("请输入需解除冻结的卡号:")
    if remove_freeze_card in auth.ATM_CARD_LIST:
        mod_user_data=db_handler.read_data(remove_freeze_card)
        mod_user_data["freeze"] = False
        db_handler.write_data(remove_freeze_card, mod_user_data)
        atm_log.info("Remove freeze card %s successful!"%mod_user_data["card_id"])
    else:
        print("抱歉，您输入的卡号不在系统中...")