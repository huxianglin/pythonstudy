#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-18
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

# import os
# import sys
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)
from shop_module import auth
from shop_module import logger
from shop_module import admin
from shop_module import goods_show
from shop_module import shop_cart

shop_log=logger.logger("shop_log")



# 存储的数据格式如下:
# data={
#         "user_id":"123456",
#         "password":"8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
#         "user_name":"张全蛋",
#         "privilege":"admin",
#         "freeze": False,
#         "shop_cart":{}
#     }


@auth.shop_auth_log(shop_log)
def main():
    # admin.admin(shop_log)
    #goods_show.show_goods(shop_log,user_log)
    user_log=logger.logger(auth.INIT_DATA["shop_user_id"])
    # shop_cart.shop_cart(shop_log,user_log)
    operations={"购物":goods_show.show_goods,"购物车":shop_cart.shop_cart,"管理":admin.admin}
    while True:
        num_operations=[]
        for i,j in enumerate(sorted(operations),1):
            print(i,j)
            num_operations.append(j)
        print()
        operation=input("请输入您的操作,b退出:").strip()
        if operation in operations  or operation.isdigit():
            if operation.isdigit:
                operation=int(operation)
                if 1<=operation<=len(num_operations):
                    operation=num_operations[operation-1]
                else:
                    print("您输入的操作不在系统中...")
                    continue
            for i in operations:
                if operation == "管理":
                    operations[operation](shop_log)
                    break
                elif operation == i:
                    operations[operation](shop_log,user_log)
        elif operation == "b":
            auth.INIT_DATA["shop_user_id"]=""
            auth.INIT_DATA["shop_user_flag"]=False
            auth.INIT_DATA["shop_user_admin"]=False
            break
        else:
            print("您输入的操作不在本系统中...")

if __name__=="__main__":
    main()
