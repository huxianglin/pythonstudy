#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-17
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import os
import json
from conf import settings


def file_db_write(file_name,data):
    file_path=os.path.join(settings.DATABASE["path"],file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
def file_db_read(file_name):
    file_path=os.path.join(settings.DATABASE["path"],file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def mysql_write(*args,**kwargs):
    pass

def mysql_read(*args,**kwargs):
    pass

if settings.DATABASE["engine"]=="file_storage":
    read_data,write_data=file_db_read,file_db_write
elif settings.DATABASE["engine"]=="mysql":
    read_data,write_data=mysql_read,mysql_write