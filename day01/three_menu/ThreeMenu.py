#!/usr/bin/env python
# encoding:utf-8
# author: huxianglin

import json
'''
通过load_data函数获取json文件中保存的全国行政区数据
'''
def load_data():
    data_file=open("省地县.json","r",encoding='utf-8')#以utf-8编码打开json文件对象
    data=json.load(data_file)#将该文件对象中的数据转换成json格式的数据
    data_file.close()#关闭文件对象
    return data#返回从文件中获取到的数据

if __name__=="__main__":
    data=load_data()#通过调用load_data函数获取数据
    print("******全国行政区查询系统******")
    while True:
        province_info=[]#定义该列表用来存储省份名称和编号对应关系
        for province in range(0,len(data)):#输出省级行政区名称
            print(province,data[province]["name"])
            province_info.append(data[province]["name"])#存储省份名称与编号对应关系
        province_name=input("请输入要查询的省份名称或编号,退出请按q:").strip()#获取用户输入对象
        if str.isdigit(province_name):#假如用户输入的是编号，那么按照如下方式进入二级菜单
            while True:
                city_info=[]#用来存储地级市名称和编号对应关系
                for city in range(0,len(data[int(province_name)]["city"])):#输出某省地级市名称
                    print(city,data[int(province_name)]["city"][city]["name"])
                    city_info.append(data[int(province_name)]["city"][city]["name"])#存储地级市名称与编号对应关系
                city_name=input("请输入要查询的地级市名称或编号,返回上层请按b，退出请按q:").strip()#获取用户输入对象
                if str.isdigit(city_name):#如果用户输入的是编号，那么按照如下方式处理
                    while True:
                        for area in range(0,len(data[int(province_name)]["city"][int(city_name)]["area"])):#输出县级市名称
                            print(area,data[int(province_name)]["city"][int(city_name)]["area"][area])
                        area_name=input("返回上层请按b，退出请按q:").strip()#获取用户输入对象
                        if area_name=="b":#判断用户是否想反回上一层
                            break
                        elif area_name=="q":#判断用户是否要退出程序
                            exit()
                        else:
                            print("输入有误，请重新输入。。。")
                elif city_name=="b":#判断用户是否想反回上一层
                    break
                elif city_name=="q":#判断用户是否要退出程序
                    exit()
                else:#用户如果输入的是字符串，则使用下面方法处理
                    if city_name in city_info:#判断用户输入的字符串是否存在于地级市与编号对应关系列表中
                        city_name=city_info.index(city_name)#如果在列表中，将用户输入的城市名称转换成编号
                        while True:#从这开始后面逻辑和前面基本一致，就不写注释了
                            for area in range(0,len(data[int(province_name)]["city"][int(city_name)]["area"])):
                                print(area,data[int(province_name)]["city"][int(city_name)]["area"][area])
                            area_name=input("返回上层请按b，退出请按q:").strip()
                            if area_name=="b":
                                break
                            elif area_name=="q":
                                exit()
                            else:
                                print("输入有误，请重新输入。。。")
                    else:
                        print("输入有误，请重新输入。。。")
        elif province_name=="q":
            exit()
        else:
            if province_name in province_info:
                province_name=province_info.index(province_name)
                while True:
                    city_info=[]
                    for city in range(0,len(data[int(province_name)]["city"])):
                        print(city,data[int(province_name)]["city"][city]["name"])
                        city_info.append(data[int(province_name)]["city"][city]["name"])
                    city_name=input("请输入要查询的地级市名称或编号,返回上层请按b，退出请按q:").strip()
                    if str.isdigit(city_name):
                        while True:
                            for area in range(0,len(data[int(province_name)]["city"][int(city_name)]["area"])):
                                print(area,data[int(province_name)]["city"][int(city_name)]["area"][area])
                            area_name=input("返回上层请按b，退出请按q:").strip()
                            if area_name=="b":
                                break
                            elif area_name=="q":
                                exit()
                            else:
                                print("输入有误，请重新输入。。。")
                    elif city_name=="b":
                        break
                    elif city_name=="q":
                        exit()
                    else:
                        if city_name in city_info:
                            city_name=city_info.index(city_name)
                            while True:
                                for area in range(0,len(data[int(province_name)]["city"][int(city_name)]["area"])):
                                    print(area,data[int(province_name)]["city"][int(city_name)]["area"][area])
                                area_name=input("返回上层请按b，退出请按q:").strip()
                                if area_name=="b":
                                    break
                                elif area_name=="q":
                                    exit()
                                else:
                                    print("输入有误，请重新输入。。。")
                        else:
                            print("输入有误，请重新输入。。。")
            else:
                print("输入有误，请重新输入。。。")