#!/usr/bin/env python
# encoding:utf-8
# author: huxianglin

'''
通过auth_user函数判断用户名密码是否正确，返回相应的处理结果
'''
def auth_user(username,password):
    user_file=open("./user.txt","r") #以只读方式打开文件对象
    user_list=[]        #声明用户列表，将用户名和密码都存储在该列表中
    for line in user_file:  #通过循环将文件对象中的每一行内容取出来，并赋值给line变量
        user_list.append(line.split()) #将每一行的用户名和密码转换成一个列表存储进入user_list列表中
    user_file.close() #关闭文件
    user_num=0  #通过该变量计数，判断传递进入的用户名是否存在于user.txt文件中
    for user_info in user_list: #通过从user_list中获取每一个用户名，密码的列表
        if username == user_info[0]: #判断传入进来的用户名是否是该用户的用户名
            if password == user_info[1]: #判断传入进来的密码是否是该用户的密码
                return True #如果用户名和密码都匹配正确，那么返回true
            else:
                return 'pwd_err' #否则返回密码错误
        user_num += 1 #如果传递进来的用户名和该用户不匹配，则该计数加一
    if user_num == len(user_list): #判断计数是否等于用户列表的长度，如果等于，则该传递进来的用户不在该用户列表中
        return 'no_user' #返回用户不存在的flag

'''
通过add_black_user函数将用户连续三次输错密码的用户添加到用户黑名单中
'''
def add_black_user(user):
    black_user_file=open('./black_user.txt','a') #以追加方式打开黑名单文件对象
    black_user_file.write(user+'\n') #将传入进来的用户名追加到黑名单文件的末尾
    black_user_file.close() #关闭黑名单文件

'''
通过auth_balck_user判断用户是否在黑名单中，如果在黑名单中，则返回true，否则返回false
'''
def auth_black_user(user):
    black_user_file=open('./black_user.txt','r') #以只读方式打开黑名单文件对象
    black_user_list=[] #定义黑名单用户列表
    for line in black_user_file: #遍历黑名单文件对象，将每一行数据读取后存放到变量line中
        black_user_list.append(line.strip()) #将line中的换行符去除，并添加到黑名单用户列表中
    black_user_file.close() #关闭黑名单文件对象
    if user in black_user_list: #判断传入的用户名是否在黑名单用户列表中，如果存在返回true否则返回false
        return True
    else:
        return False

if __name__ == '__main__':
    print("""
    *******************************
    * welcome to my login system! *
    *******************************""") #打印一个欢迎头部
    while True: #通过死循环来实现用户的持续输入
        username=input("login:").strip() #将用户输入的用户名存入变量username中
        password=input("password:").strip() #将用户输入的密码存入变量password中
        flag=auth_user(username,password) #通过auth_user函数判断该用户名密码的状态
        if flag == "no_user": #假如返回no_user则说明该用户不存在，结束该循环，进入下一次循环
            print("抱歉，用户%s不存在，请重新输入。。。" %username)
            continue
        elif auth_black_user(username): #通过auth_black_user函数的返回值判断该用户是否是黑名单用户，若是，提示并退出程序
            print("抱歉，该用户已被拉入黑名单，程序即将退出。。。")
            exit()
        elif flag == "pwd_err": #如果输入的密码错误，则进入下面的判断密码输入错误次数的代码段中
            print("抱歉，您输入的密码错误")
            relogin_num=1 #计数器，假如用户密码输入错误超过3次，那么将锁定该用户
            for i in range(0,2): #在用户第一次输入密码错误之后，判断余下两次输入密码是否正确
                password=input("password:").strip() #获取用户新输入的密码
                if auth_user(username,password) == "pwd_err": #如果用户新输入的密码还是错误的话，计数器加一，并结束该循环，进入下一次密码判断
                    print("抱歉，您输入的密码错误")
                    relogin_num+=1
                    continue
                elif auth_user(username,password) == True: #假如用户名密码都输入正确的话判断该用户是否在黑名单中
                    print("恭喜，登录成功！")
                    exit()
            if relogin_num == 3: #如果循环结束，说明用户连续三次输入错误密码，则将该用户添加进入黑名单中并关闭程序
                print("你已连续三次输入密码错误，用户%s已被拉入黑名单中!程序即将关闭。。。" %username)
                add_black_user(username)
                exit()
        else:
            print("恭喜，登录成功！")
            exit()