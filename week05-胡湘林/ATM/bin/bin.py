#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-13
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/
import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print(BASE_DIR)
from ATM.bin import atm
from shop.shop_bin import shop

def main():
    while True:
        operations={"ATM":atm.atm,"购物":shop.shop}
        num_operations=[]
        for i,j in enumerate(operations,1):
            print(i,j)
            num_operations.append(j)
        print()
        operation=input("请输入您的操作,q退出:").strip()
        if operation == "q":
            break
        elif operation in operations or operation.isdigit():
            if operation.isdigit():
                operation=int(operation)
                if 1<=operation<=len(num_operations):
                    operation=num_operations[operation-1]
                else:
                    print("您的输入有误...")
                    continue
            for i in operations:
                if operation == i:
                    operations[operation]()
        else:
            print("您的输入有误...")


if __name__=="__main__":
    main()





