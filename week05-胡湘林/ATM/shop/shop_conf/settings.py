#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-18
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import os
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


USER_DATABASE = {
    "name":"users",
    "path": os.path.join(os.path.join(BASE_DIR,"shop_data"),"users_info")
}
DATABASE_ENGINE="file_storage"  # support mysql in the future
GOODS_DATABASE={
    "name":"goods",
    "path": os.path.join(os.path.join(BASE_DIR,"shop_data"),"goods_data.json")
}

LOG_INFO = {
    "shop_path":os.path.join(BASE_DIR,"shop_logs"),
    "LOG_LEVEL":logging.INFO
}

BANK_CARD="666666"