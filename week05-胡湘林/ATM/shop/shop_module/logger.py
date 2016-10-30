#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-18
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import logging
import os
from shop_conf import settings

def logger(logger_file):
    logger_path=os.path.join(settings.LOG_INFO["shop_path"],logger_file)
    print(logger_path)
    log=logging.getLogger(logger_file)
    log.setLevel(settings.LOG_INFO["LOG_LEVEL"])
    log.handlers=[]  # 清空log对象中的handlers

    sh=logging.StreamHandler()
    sh.setLevel(settings.LOG_INFO["LOG_LEVEL"])

    fh=logging.FileHandler(logger_path)
    fh.setLevel(settings.LOG_INFO["LOG_LEVEL"])

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    log.addHandler(sh)
    log.addHandler(fh)

    return log