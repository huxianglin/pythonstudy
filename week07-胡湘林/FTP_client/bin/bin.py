#!/usr/bin/env python
# encoding:utf-8
# __author__: bin
# date: 2016/10/7 11:14
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import os
import sys
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from source import conn_client

if __name__=="__main__":
    parser = argparse.ArgumentParser()  # 接收启动脚本参数
    parser.add_argument("--operation", help="operation",type=str,default="")  # 接收操作命令
    parser.add_argument("--file", help="file",type=str,default="")  # 接收文件名称
    args = parser.parse_args()  # 获取接收变量对象
    operation=args.operation  # 获取操作命令
    file=args.file  # 获取操作文件名称
    if operation and file:  # 两个都有值的时候
        if operation in ["upload","download"]:  # 操作是上传或下载的时候
            conn_client.conn_server([operation,file])  # 把命令和文件名拼接成列表传递给连接函数
        else:
            raise Exception("输入的参数有误，请输入正确参数...")  # 抛出异常
    else:
        conn_client.conn_server()  # 没满足传递两个参数进来时，正常执行脚本
