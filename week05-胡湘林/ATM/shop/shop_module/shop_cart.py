#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-18
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

from shop_module import auth
from shop_module import db_handler
from shop_conf import settings
import os,sys
FATHER_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(FATHER_DIR)
from ATM.module import trans_action

def shop_cart(shop_log,user_log):
    while True:
        user_data=db_handler.read_user(auth.INIT_DATA["shop_user_id"])
        print("购物车中的商品信息如下:")
        for i in user_data["shop_cart"]:
            print("\t".join(("商品名:",str(user_data["shop_cart"][i]["good_name"]),"商品单价:",str(user_data["shop_cart"][i]["good_unit_price"]),"商品数量:",str(user_data["shop_cart"][i]["good_count"]))))
        print("1 删除商品\t2 结账\tb 返回")
        operation=input("请输入您的操作:").strip()
        if operation in ["1","删除商品"]:
            del_goods(user_data,shop_log,user_log)
        elif operation in ["2","结账"]:
            break
        elif operation == "b":
            return
        else:
            print("您输的输入不在系统中...")
            continue

    sum_money=0
    for i in user_data["shop_cart"]:
        sum_money+=user_data["shop_cart"][i]["good_unit_price"]*user_data["shop_cart"][i]["good_count"]
    pay_result=trans_action.pay_money(sum_money,settings.BANK_CARD)
    if pay_result:
        user_log.info("User ID:%s pay %s RMB shop %s Successful!"%(auth.INIT_DATA["shop_user_id"],sum_money,user_data["shop_cart"]))
        shop_log.info("User ID:%s pay %s RMB shop %s Successful!"%(auth.INIT_DATA["shop_user_id"],sum_money,user_data["shop_cart"]))
        user_data["shop_cart"]={}
        db_handler.write_user(auth.INIT_DATA["shop_user_id"],user_data)
    else:
        user_log.info("User ID:%s pay %s RMB shop %s failed!Don't have enough money!"%(auth.INIT_DATA["shop_user_id"],sum_money,user_data["shop_cart"]))
        shop_log.info("User ID:%s pay %s RMB shop %s failed!Don't have enough money!"%(auth.INIT_DATA["shop_user_id"],sum_money,user_data["shop_cart"]))


def del_goods(user_data,shop_log,user_log):
    del_good=input("请输入您要删除的商品:").strip()
    if del_good in user_data["shop_cart"]:
        del user_data["shop_cart"][del_good]
        db_handler.write_user(auth.INIT_DATA["shop_user_id"],user_data)
        print("商品:%s已被删除!"%del_good)
        shop_log.info("User ID:%s from shop cart del good %s successful!"%(auth.INIT_DATA["shop_user_id"],del_good))
        user_log.info("From shop cart del good %s successful!"%del_good)
    else:
        print("抱歉,您输入的商品名不在购物车中...")