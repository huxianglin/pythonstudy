#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-18
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import hashlib

def encry_passwd(passwd):
    sha256_obj = hashlib.sha256()
    sha256_obj.update(passwd.encode("utf-8"))
    return sha256_obj.hexdigest()

# print(encry_passwd("123456"))