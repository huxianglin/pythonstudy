#!/usr/bin/env python
# encoding:utf-8
# __author__: commons
# date: 2016/10/7 0:56
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/
import os
import hashlib
import time
from conf import settings

def get_file_hash(filepath):
    file_size=os.stat(filepath).st_size
    read_size=0
    md5_obj=hashlib.md5()
    with open(filepath,"rb") as f:
        while read_size != file_size:
            data=f.read(1024)
            md5_obj.update(data)
            read_size+=len(data)
    return md5_obj.hexdigest()

if isinstance(settings.PROGRESS_LINE_SIZE,int):
    if 1 <= settings.PROGRESS_LINE_SIZE <= 100:
        star_list=[i for i in range(1,settings.PROGRESS_LINE_SIZE+1)]
    else:
        raise Exception("参数设置错误...PROGRESS_LINE_SIZE范围在1-100")
else:
    raise Exception("参数设置错误...PROGRESS_LINE_SIZE必须是整数")

def show_progress_line(send_que,totol_size):
    """进度条"""
    send_size=send_que.get()
    while send_size/totol_size<=1:
        time.sleep(settings.PROGRESS_LINE_PERIOD)
        percent=int(send_size * 100 / totol_size)
        space_len=" "*int(settings.PROGRESS_LINE_SIZE-settings.PROGRESS_LINE_SIZE*(percent/100)+3)
        message="\t".join((space_len.join(("".join(("="*int(percent/100*settings.PROGRESS_LINE_SIZE),">")),"{percent}%".format(percent=percent))),time.ctime()))
        print(message,end="\n",flush=True)
        if send_size==totol_size:
            print("Translate is finish!")
            break
        send_size=send_que.get()