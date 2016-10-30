#!/usr/bin/env python
# encoding:utf-8
# __author__: bin
# date: 2016/10/7 10:28
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from source import conn_server

if __name__=="__main__":
    conn_server.main()