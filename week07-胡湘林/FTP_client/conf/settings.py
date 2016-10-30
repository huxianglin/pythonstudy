#!/usr/bin/env python
# encoding:utf-8
# __author__: settings
# date: 2016/10/7 0:18
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/
import os
import sys
SERVER_IP="127.0.0.1"
SERVER_PORT=8000
HOMEDIR=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"data")
OPER_SYS="linux" if "posix" in sys.builtin_module_names else "win"
PROGRESS_LINE_SIZE=100  # 设置进度条最大长度(在1-100之间)
PROGRESS_LINE_PERIOD=1  # 设置进度条的刷新周期