#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-18
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import os
from shop_conf import settings
from shop_module import auth
from shop_module import encry_passwd
from shop_module import db_handler

def admin(shop_log):
    while True:
        operations_dict={"添加":__add_user__,"删除":__del_user__,"修改":__mod_user__,"查询":__que_user__,"修改密码":__mod_passwd__,"解冻":__remove_freeze__}
        num_operations=[]
        for i,j in enumerate(sorted(operations_dict),1):
            print(i,j,end="\t")
            num_operations.append(j)
        print()
        operation=input("请输入您选择的操作,b返回:").strip()
        if operation=="b":
            break
        elif operation in operations_dict or operation.isdigit():
            if operation.isdigit():
                operation=int(operation)
                if 1<=operation<=len(operations_dict):
                    operation=num_operations[operation-1]
                else:
                    print("您输入的操作不在本系统中...")
            [operations_dict[operation](shop_log) for i in operations_dict if i==operation]

        else:
            print("您输入的操作不在本系统中...")

def __add_user__(shop_log):
    while True:
        user_dict={"user_id":"","password":"","user_name":"","privilege":"","freeze":False,"shop_cart":{}}
        user_id = input("请输入6位用户名,b返回:").strip()
        if user_id == "b":
            break
        elif len(user_id) != 6 or not user_id.isdigit():
            print("抱歉，您输入的用户ID有误...")
        elif user_id in auth.INIT_DATA["shop_user_list"]:
            print("抱歉，您输入的用户ID已存在...")
        else:
            user_dict["user_id"]=user_id
            password = input("请输入密码:").strip()
            user_dict["password"] = encry_passwd.encry_passwd(password)
            while True:
                privilege = input("请输入用户权限，user或admin:").strip()
                if privilege not in ["user", "admin"]:
                    print("抱歉，您输入的权限不合法....")
                else:
                    user_dict["privilege"] = privilege
                    break
            user_dict["user_name"] = input("请输入用户名:").strip()
            db_handler.write_user(user_id, user_dict)
            shop_log.info("Add new user %s successful!"%user_dict["user_id"])
            auth.INIT_DATA["shop_user_list"]=os.listdir(settings.USER_DATABASE["path"])

def __del_user__(shop_log):
    while True:
        for i, j in enumerate(auth.INIT_DATA["shop_user_list"], 1):
            print(i, j)
        del_operation = input("请输入要删除的用户ID,b返回:").strip()
        if del_operation == "b":
            break
        elif del_operation in auth.INIT_DATA["shop_user_list"]:
            os.remove(os.path.join(auth.INIT_DATA["shop_user_path"],del_operation))
            auth.INIT_DATA["shop_user_list"]=os.listdir(settings.USER_DATABASE["path"])
            shop_log.info("Del user %s successful!"%del_operation)
        else:
            print("抱歉，您的输入有误...")

def __mod_user__(shop_log):
    while True:
        for i, j in enumerate(auth.INIT_DATA["shop_user_list"], 1):
            print(i, j)
        mod_user_id = input("请输入要修改的用户ID,b返回:").strip()
        if mod_user_id == "b":
            break
        elif mod_user_id in auth.INIT_DATA["shop_user_list"]:
            mod_user_data=db_handler.read_user(mod_user_id)
            print("用户ID:%s的信息如下:" % mod_user_id)
            print("密码:xxx 权限:%s 用户名:%s 冻结:%s" %
                  (mod_user_data["privilege"], mod_user_data["user_name"], mod_user_data["freeze"]))
            mod_info_list = input("请按照如下选项进行修改，每项之间用空格分隔:\n密码 权限(user or admin) 用户名 "
                                  "冻结(true or false)\n>>>").strip().split()
            if len(mod_info_list) == 4 and mod_info_list[1] in ["user", "admin"] and  mod_info_list[3] in ["true", "false"]:
                print("用户ID:%s更新成功" % mod_user_id)
                mod_info_list[0] = encry_passwd.encry_passwd(mod_info_list[0])
                if mod_info_list[3] == "true":
                    mod_info_list[3] = True
                else:
                    mod_info_list[3] = False
                mod_info_list.reverse()
                for i in ["password","privilege","username","freeze"]:
                    mod_user_data[i]=mod_info_list.pop()
                db_handler.write_user(mod_user_id, mod_user_data)
                shop_log.info("Modefy user ID: %s successful!"%mod_user_data["user_id"])
            else:
                print("抱歉，您的输入不符合格式...")
        else:
            print("抱歉，您的输入有误...")

def __que_user__(shop_log):
    while True:
        for i, j in enumerate(auth.INIT_DATA["shop_user_list"], 1):
            print(i, j)
        queue_user_id = input("请输入要查询的用户ID,b返回:").strip()
        if queue_user_id in auth.INIT_DATA["shop_user_list"]:
            que_user_info=db_handler.read_user(queue_user_id)
            print("用户ID:%s的信息如下:" % queue_user_id)
            print("密码:xxx 权限:%s 用户名:%s 冻结:%s" %
                  (que_user_info["privilege"], que_user_info["user_name"],que_user_info["freeze"]))
            shop_log.info("Queue user ID %s successful!" % que_user_info["user_id"])
        elif queue_user_id == "b":
            break
        else:
            print("抱歉，请输入正确的用户ID...")

def __mod_passwd__(shop_log):
    mod_user_id = input("请输入修改密码的用户ID:")
    if mod_user_id in auth.INIT_DATA["shop_user_list"]:
        mod_user_data=db_handler.read_user(mod_user_id)
        mod_password = input("请输入新密码:")
        mod_user_data["password"] = encry_passwd.encry_passwd(mod_password)
        db_handler.write_user(mod_user_id, mod_user_data)
        shop_log.info("Modefy user ID %s password successful!"%mod_user_data["user_id"])
    else:
        print("抱歉，您输入的用户ID不在系统中...")

def __remove_freeze__(shop_log):
    remove_freeze_user = input("请输入需解除冻结的用户ID:")
    if remove_freeze_user in auth.INIT_DATA["shop_user_list"]:
        mod_user_data=db_handler.read_user(remove_freeze_user)
        mod_user_data["freeze"] = False
        db_handler.write_user(remove_freeze_user, mod_user_data)
        shop_log.info("Remove freeze card %s successful!"%mod_user_data["user_id"])
    else:
        print("抱歉，您输入的卡号不在系统中...")