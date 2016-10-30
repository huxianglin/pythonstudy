#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-17
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import os
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASE = {
    "engine": "file_storage", #support mysql in the future
    "name":"users",
    "path": os.path.join(os.path.join(BASE_DIR,"data"),"users_info")
}


LOG_INFO = {
    "ATM_path":os.path.join(BASE_DIR,"logs"),
    "LOG_LEVEL":logging.INFO
}

TRANSACTION_TYPE = {
    "repay":{"action":"plus", "interest":0},
    "withdraw":{"action":"minus", "interest":0.05},
    "transfer":{"action":"minus", "interest":0.05},
    "consume":{"action":"minus", "interest":0}
}
