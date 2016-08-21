#!/usr/bin/env python
# encoding:utf-8
# author: huxianglin

import json

def load_data():
    data_file=open("省地县.json","r",encoding='utf-8')
    data=json.load(data_file)
    data_file.close()
    return data

if __name__=="__main__":
    data=load_data()
    print("******全国行政区查询系统******")
    while True:
        province_info=[]
        for province in range(0,len(data)):
            print(province,data[province]["name"])
            province_info.append(data[province]["name"])
        province_name=input("请输入要查询的省份名称或编号,退出请按q:").strip()
        if str.isdigit(province_name):
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