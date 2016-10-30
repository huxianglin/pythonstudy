#!/usr/bin/env python
# encoding:utf-8
# __author__: settings
# date: 2016/10/2 14:02
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/
import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_DATA_DIR=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"clients_data")
CLI_HOME_DIR=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"clients_home")

IPADDR="0.0.0.0"
PORT=8000

PROGRESS_LINE_SIZE=100  # 设置进度条最大长度(在1-100之间)
PROGRESS_LINE_PERIOD=1  # 设置进度条的刷新周期