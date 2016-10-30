#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-18
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/


from shop_module import db_handler
from shop_module import auth

def show_goods(shop_log,user_log):
    goods_data=db_handler.read_goods()
    user_data=db_handler.read_user(auth.INIT_DATA["shop_user_id"])
    while True:
        num_goods=[]
        for i,j in enumerate(sorted(goods_data),1):
            print(i,j,end="\t")
            num_goods.append(j)
        print()
        choice1=input("请输入您的选择,b返回:").strip()
        if choice1 in goods_data or choice1.isdigit():
            if choice1.isdigit():
                choice1=int(choice1)
                if 1<=choice1<=len(num_goods):
                    choice1=num_goods[choice1-1]
                else:
                    print("您的输入有误...")
                    continue
            while True:
                num_goods=[]
                for i,j in enumerate(sorted(goods_data[choice1].items()),1):
                    print(" ".join((str(i),"商品名:",j[0],"\t\t价格:",str(j[1]),"元")))
                    num_goods.append(j[0])
                choice2=input("请输入您的选择,b返回:").strip()
                if choice2 in goods_data[choice1] or choice2.isdigit():
                    if choice2.isdigit():
                        choice2=int(choice2)
                        if 1<=choice2<=len(num_goods):
                            choice2=num_goods[choice2-1]
                        else:
                            print("您的输入有误...")
                            continue
                    if not user_data["shop_cart"].get(choice2):
                        print(choice1,choice2)
                        user_data["shop_cart"][choice2]={"good_name":choice2,"good_count":1,"good_unit_price":goods_data[choice1][choice2]}
                        db_handler.write_user(auth.INIT_DATA["shop_user_id"],user_data)
                        shop_log.info("User ID:%s append %s to shop cart!"%(auth.INIT_DATA["shop_user_id"],choice2))
                        user_log.info("append %s to shop cart!"%choice2)
                        print("添加%s 到购物车成功!"%choice2)
                    else:
                        user_data["shop_cart"][choice2]["good_count"]+=1
                        db_handler.write_user(auth.INIT_DATA["shop_user_id"],user_data)
                        shop_log.info("User ID:%s append %s to shop cart!"%(auth.INIT_DATA["shop_user_id"],choice2))
                        user_log.info("append %s to shop cart!"%choice2)
                elif choice2 == "b":
                    break
        elif choice1 == "b":
            break
        else:
            print("您的输入有误...")
            continue
