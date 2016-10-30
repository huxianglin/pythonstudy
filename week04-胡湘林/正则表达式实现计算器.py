#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-12
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import re
import time

"""定义装饰器，计算器执行时间"""


def show_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print("计算执行时间:%ss" % (end_time - start_time))

    return wrapper


def check_out(expression):
    """检查函数，简单的检查表达式是否合法"""
    char_flag, parenthesis_flag = False, False  # 定义非法字符标记及括号检查标记
    char_list = re.findall("[^0-9\+\-\*/(). ]", expression)  # 获取表达式中的非法字符列表
    char_flag = True if not char_list else print("输入表达式中含有非法字符%s..." % char_list)  # 列表为空，则没有非法字符
    left_parenthesis_list = []  # 定义存储左括号列表
    for i in expression:  # 遍历表达式，获取每一个字符
        if i == ")":  # 如果获取到的是右括号
            if left_parenthesis_list:  # 判断左括号列表中是否有内容
                left_parenthesis_list.pop()  # 如果有内容，弹出一个左括号
            else:  # 否则，说明右括号和左括号不匹配（可能是右括号在左括号之前出现）
                print("左右括号不匹配...")
                break
        elif i == "(":  # 如果获取到的是左括号，则将左括号添加到左括号列表中
            left_parenthesis_list.append(i)
    parenthesis_flag = True if not left_parenthesis_list else print(
        "左右括号不匹配...")  # 遍历完成之后判断左括号列表中是否还有括号，如果有，则说明左括号多了，否则左右括号匹配
    if char_flag and parenthesis_flag:  # 没有非法字符并且括号匹配时，返回True,检查通过，否则检查不通过
        return True
    else:
        return False


def format_expression(expression):
    """标准化输入的表达式，去除一些计算不需要的字符"""
    expression = expression.replace(" ", "")  # 去除空格
    expression = expression.replace("+-", "-")  # 将+-替换为-
    expression = expression.replace("--", "+")  # 将--替换为+
    return expression


def remove_parenthesis(expression):
    """
    定义去括号函数，这个函数的作用就是循环在表达式中寻找最内层的括号，计算括号内的表达式，将结果替换到找到的括号位置
    直到所有括号及括号内的内容都被替换成计算结果之后，再对没有括号的表达式进行加减乘除运算，得到最后结果后返回给主调函数
    """
    while re.search("\([^()]+\)", expression):
        rst = re.search("\([^()]+\)", expression).group()  # 寻找到最里层括号及其内部表达式
        remove_parenthesis_rst = re.sub("[()]", "", rst)  # 将找到的表达式的括号去掉
        mul_div_rst = mul_div(remove_parenthesis_rst)  # 调用乘除函数，将表达式中的乘除运算全部计算并替换成计算结果
        sum_reduce_rst = sum_reduce(mul_div_rst)  # 调用加减函数，将之前计算到一半的表达式进行加减运算，得到计算结果
        expression = expression.replace(rst, sum_reduce_rst)  # 将计算结果替换到表达式中之前找到的最里层括号及其内部的表达式
    else:
        mul_div_rst = mul_div(expression)  # 最后将不包含括号的表达式传递进入乘除函数全部计算完成后，表达式将只剩下+-法了
        sum_reduce_rst = sum_reduce(mul_div_rst)  # 将只剩下+-号的表达式传入加减法运算函数，获取到最后的计算结果
        return sum_reduce_rst  # 返回最后的计算结果


def sum_reduce(expression):
    """
        计算传入表达式中的所有加减法，并将结果替换进去
    """
    if "+--" in expression:  # 如果传入的表达式中含有+--，则替换成+
        expression = expression.replace("+--", "+")
    if "---" in expression:  # 如果传入的表达式中含有---，则替换成-
        expression = expression.replace("---", "-")
    while re.search("-?\d+(\.\d*)?[+-]-?\d+(\.\d*)?", expression):  # 匹配+-法以及其左右的操作数
        rst = re.search("-?\d+(\.\d*)?[+-]-?\d+(\.\d*)?", expression).group()  # 找到匹配正则的那段表达式
        if "+" in rst:  # 如果+包含在表达式中，执行加法，并将结果替换到刚刚找到的表达式中
            left, right = [float(i) for i in rst.split("+")]
            new_rst = str(left + right)
            expression = expression.replace(rst, new_rst)
        elif "-" in rst:

            """
            如果-包含在表达式中，那么存在如下四种不同情况需要处理：
                1.左边操作数是负数，右边操作数是负数
                2.左边操作数是负数，右边操作数是正数
                3.左边操作数是正数，右边操作数是负数
                4.左边操作数是正数，右边操作数是正数
            """
            if rst[0] == "-":
                if "--" in rst:  # 第一种情况
                    rst_2 = re.sub("^-", "", rst)
                    rst_2 = rst_2.replace("--", "-")
                    left, right = [float(i) for i in rst_2.split("-")]
                    left *= -1
                    right *= -1
                    new_rst = str(left - right)
                    expression = expression.replace(rst, new_rst)
                else:  # 第二种情况
                    rst_2 = re.sub("^-", "", rst)
                    left, right = [float(i) for i in rst_2.split("-")]
                    left *= -1
                    new_rst = str(left - right)
                    expression = expression.replace(rst, new_rst)
            else:
                if "--" in rst:  # 第三种情况
                    rst_2 = rst.replace("--", "-")
                    left, right = [float(i) for i in rst_2.split("-")]
                    right *= -1
                    new_rst = str(left - right)
                    expression = expression.replace(rst, new_rst)
                else:  # 第四种情况
                    left, right = [float(i) for i in rst.split("-")]
                    new_rst = str(left - right)
                    expression = expression.replace(rst, new_rst)
    return expression


def mul_div(expression):
    """
        计算表达式中的乘除法，并将结果替换到表达式中
    """
    while re.search("\d+(\.\d*)?[*/]-?\d+(\.\d*)?", expression):  # 找到表达式中的乘除法并循环替换，直到找不到为止
        rst = re.search("\d+(\.\d*)?[*/]-?\d+(\.\d*)?", expression).group()  # 找到乘除法及其两边的操作数
        if "*" in rst:  # 如果*在表达式中，则计算乘法，并将结果替换到表达式中
            left, right = [float(i) for i in rst.split("*")]
            new_rst = str(left * right)
            expression = expression.replace(rst, new_rst)
        elif "/" in rst:  # 如果/在表达式中，则判断右操作数是否为0，不为零，正常计算，否则，报出错误并停止计算
            left, right = [float(i) for i in rst.split("/")]
            if right != 0:  #右操作数不为0时
                new_rst = str(left / right)
                expression = expression.replace(rst, new_rst)
            else:  # 右操作数为0时
                print("除数不能为零...")
                break
    return expression


@show_time
def main():
    expression = "1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )"
    if check_out(expression):  # 判断表达式是否通过检查
        expression = format_expression(expression)  # 将表达式标准化
        print(expression)  # 打印标准化后的表达式
        print("计算结果:%s" % remove_parenthesis(expression))  # 执行计算，并打印计算结果
        print("eval计算结果:%s" % eval(expression))  # 执行eval计算并打印计算结果


if __name__ == "__main__":  # 测试函数
    main()
