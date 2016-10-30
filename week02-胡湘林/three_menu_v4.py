#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-08-27
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/
'''数据格式如下:
data={
        "江西省":{
                "南昌市":["湾里区","新建县"]
                }
        }
'''
import json
'''通过json.load获取数据并返回'''
def read_data():
    data=json.load(open("省地县.json","r"))
    return data
'''通过json.dump将数据存储到文件中，也可使用json.dumps（将字典转换成字符串，再通过write写入）'''
def write_data(data):
    with open("省地县.json","w",encoding="utf-8") as f:
        # f.write(json.dumps(data))
        json.dump(data,f)

if __name__ == "__main__":
    data=read_data()#通过read_data获取数据
    choice_layer=data#定义选择的层级默认等于顶级
    parents_list=[]#父亲列表进行了修改，存储的不是字典，而是用户曾经输入的父级字符串
    num_area={}#将打印出的数字和字符串关联的一个字典
    while True:
        num_area.clear()
        print("欢迎来到三级菜单系统".center(50,"*"))
        if isinstance(choice_layer,dict):
            for i,j in enumerate(sorted(choice_layer.keys()),1):#输出当前层级下属的层级名称
                if i<=5:
                    print(i,j,end="\t")
                num_area[str(i)]=j
            print()
        else:
            for i,j in enumerate(choice_layer,1):#输出当前层级下属的层级名称
                if i<=5:
                    print(i,j,end="\t")
                num_area[str(i)]=j
            print()
        choice_name=input("添加:a,删除:d,修改:m,返回上层:b,退出:q>>>").strip()
        if choice_name in choice_layer:#判断用户输入的是字符串并且在字典的key中
            if isinstance(choice_layer,dict):#判断该层数据类型是字典类型（第三层我使用列表存储）
                parents_list.append(choice_name)#在父列表中追加刚选择的名称
                choice_layer = choice_layer[choice_name]#将显示层调到选择的层
            else:
                print("已到达最后一层。。。")
        elif choice_name.isdigit():#判断用户输入的是数字
            if 0<int(choice_name)<=len(num_area):#判断用户输入的数字在num_area中
                choice_name=num_area[choice_name]#将用户输入的数字转换成字符串
                if isinstance(choice_layer,dict):#判断该层数据类型是字典类型（第三层我使用列表存储）
                    parents_list.append(choice_name)#在父列表中追加刚选择的名称
                    choice_layer = choice_layer[choice_name]#将显示层调到选择的层
                else:
                    print("已到达最后一层...")
            else:
                print("您输入的编号不在列表中...")
        elif choice_name=="a":#判断用户输入的是添加
            add_name=input("请输入要添加的名称:").strip()
            if add_name not in choice_layer:#判断用户输入的名称不在列表中
                if parents_list:#如果parents_list不为空，只有两种情况，一种是存储了一个值，一种是存储了两个值
                    if len(parents_list)==1:#存储一个值时，添加的key对应的value是一个列表
                        data[parents_list[0]][add_name]=[]
                    else:#否则，就是存储了两个值，那么添加的内容应该被追加到列表的最后
                        data[parents_list[0]][parents_list[1]].append(add_name)
                else:
                    data[add_name]={}#如果parents_list为空，说明是在最顶层添加省份，那么，添加的key对应的value是一个字典
                write_data(data)#添加完数据后将最新数据写入文件中
            else:
                print("抱歉，您输入的地区已存在...")
        elif choice_name=="d":#判断用户输入的是删除
            del_name=input("请输入要删除的名称:").strip()
            if del_name in choice_layer:#判断用户输入的名称在列表中
                if parents_list:#如果parents_list不为空，只有两种情况，一种是存储了一个值，一种是存储了两个值
                    if len(parents_list)==1:#存储一个值时，删除的是地级市，相当于删除字典的一个key
                        del data[parents_list[0]][del_name]
                    else:#否则，就是存储了两个值，那么就该pop掉用户输入的名称对应的索引值
                        data[parents_list[0]][parents_list[1]].pop(data[parents_list[0]][parents_list[1]].index(del_name))
                else:
                    del data[del_name]#如果parents_list为空，则直接删除顶层字典的一个key
                write_data(data)#将最新数据写入文件
            else:
                print("抱歉，您输入的地区不存在...")
        elif choice_name=="m":#判断用户输入的是修改
            modify_name=input("请输入要修改的地区:").strip()
            if modify_name in choice_layer:#判断用户要修改的名称在列表中
                new_modify_name=input("新的的地区名:").strip()
                if new_modify_name not in choice_layer:#判断用户修改后的名称不在列表中
                    if parents_list:#如果parents_list不为空，只有两种情况，一种是存储了一个值，一种是存储了两个值
                        if len(parents_list)==1:#存储一个值时，修改的是字典的一个key，先将该key对应的值赋给新的key，再删除该key
                            data[parents_list[0]][new_modify_name]=data[parents_list[0]][modify_name]
                            del data[parents_list[0]][modify_name]
                        else:#否则，修改的是一个列表，先将新的名称追加到列表中，再pop掉要修改的名称对应的索引
                            data[parents_list[0]][parents_list[1]].append(new_modify_name)
                            data[parents_list[0]][parents_list[1]].pop(data[parents_list[0]][parents_list[1]].index(modify_name))
                    else:#parents_list为空时，修改的是字典，将旧的key对应的值赋给新的key，之后删除旧的key
                        data[new_modify_name]=data[modify_name]
                        del data[modify_name]
                    write_data(data)#将最新数据保存到文件中
                else:
                    print("抱歉，您输入的地区名已在系统中...")
            else:
                print("抱歉，您输入的地区不存在...")
        elif choice_name == "b":#判断用户输入的是返回上层
            if parents_list:#假如parents_list不为空，判断两种情况
                if len(parents_list)==1:#只有一个值时，直接清空parents_list，令choice_layer回到顶层
                    parents_list.pop()
                    choice_layer=data
                else:#有两个值时，把最后一个值丢弃，并把choice_layer提升到第二层
                    parents_list.pop()
                    choice_layer=data[parents_list[0]]
        elif choice_name == "q":
            break
        else:
            print("Invalid input")