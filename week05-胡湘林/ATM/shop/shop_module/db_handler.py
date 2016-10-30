#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-18
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import os
import json
# import sys
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)
from shop_conf import settings

def file_user_read(file_name):
    file_path=os.path.join(settings.USER_DATABASE["path"],file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def file_user_write(file_name,data):
    file_path=os.path.join(settings.USER_DATABASE["path"],file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def file_goods_read():
    file_path=settings.GOODS_DATABASE["path"]
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def file_goods_write(data):
    file_path=settings.GOODS_DATABASE["path"]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

def mysql_write(*args,**kwargs):
    pass

def mysql_read(*args,**kwargs):
    pass

if settings.DATABASE_ENGINE=="file_storage":
    read_user,write_user,read_goods,write_goods=file_user_read,file_user_write,file_goods_read,file_goods_write
elif settings.DATABASE["engine"]=="mysql":
    read_user,write_user=mysql_read,mysql_write

# data={
#         "书籍":{"python cookbook":80,"python core":120,"python网络编程":52,"算法导论":87},
#         "电子产品":{"Iphone 7 plus":6800,"ipad mini4":2300,"mac book pro":10300,"MSI GE62":6800},
#         "汽车":{"特斯拉":980000,"丰田凯美瑞":180000,"宝马7系LI":420000},
#         "服装":{"男外套":150,"男西裤":180,"裙子":350}
#     }
# write_goods(data)