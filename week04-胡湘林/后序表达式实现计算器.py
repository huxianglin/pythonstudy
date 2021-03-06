#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-10
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/
import re
import time

isp = {"#": 0, "(": 1, ")": 6, "+": 3, "-": 3, "*": 5, "/": 5}  # 定义栈内优先级
icp = {"#": 0, "(": 6, ")": 1, "+": 2, "-": 2, "*": 4, "/": 4}  # 定义栈外优先级

"""装饰器函数，计算消耗时间"""


def show_time(func):
    def wrapper():
        start_time = time.time()
        func()
        end_time = time.time()
        print("计算器计算时间为:%ss" % (end_time - start_time))

    return wrapper


"""定义检查函数，检查计算表达式是否含有非法字符以及判断括号是否匹配"""


def checkout(expression):
    char_flag, parenthesis_flag = False, False  # 定义非法字符标记及括号检查标记
    char_list = re.findall("[^0-9\+\-\*/\(\)\.]", expression)  # 获取表达式中的非法字符列表
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


"""将表达式中的所有操作数取出，生成一个列表，并将所有操作数使用字符S替换，再判断在最开始位置的操作数
以及左括号后面第一个操作数是否为负数，如果是负数，则将获取到的该操作数的值转换成负数，并把前面的"-"删除。
返回一个使用字符S替换操作数的新的表达式以及一个存储操作数的列表"""


def replace_expression(expression):
    negative_number_flag = []  # 定义操作数负数标记列表
    num_list = re.findall("[0-9]*\.?[0-9]+", expression)  # 获取所有的操作数字符列表
    num_list = [float(i) for i in num_list]  # 将获取到的字符操作数转换成浮点型数字
    expression = re.sub("[0-9]*\.?[0-9]+", "S", expression)  # 将所有的操作数替换成字符S
    if expression[0:2] == "-S":  # 判断第一个操作数是否是负数
        negative_number_flag.append(0)  # 如果是负数，则标记该位置的操作数
        expression = re.sub("^-S", "S", expression)  # 将前面的负号删除
    s_num = 0  # 定义操作数计数位
    for i in range(2, len(expression)):  # 前面已经判断了前两位所存储的操作数，之后从第三位开始查找操作数
        if expression[i] == "S":  # 找到操作数时
            s_num += 1  # 操作数计数+1
            if expression[i - 2:i + 1] == "(-S":  # 判断操作数及其前面的字符串组合是否是(-S
                negative_number_flag.append(s_num)  # 如果判断成功，则将该计数位添加到负数标记列表中
    expression = re.sub("\(-S", "(S", expression)  # 将该位置的操作数前面的负号删除
    if negative_number_flag:  # 如果负数标记列表中含有值，则将操作数列表中相应位置的操作数变成负数
        num_list = [num_list[i] * -1 if i in negative_number_flag else num_list[i] for i in range(len(num_list))]
    return expression, num_list  # 返回新的表达式以及操作数列表


"""将中序表达式转换成后序表达式，并将之前使用的S占用的操作数位置转换成实际的操作数。这里的将中序表达式转换成
后序表达式的原则遵循如下原则：
    1.通过之前定义的站内和栈外优先级的两个字典，确定操作符的优先级
    2.如果是操作数，直接压到后序表达式列表中
    3.如果是操作符，则遵循如下原则：
        3.1.如果取到的操作符栈外优先级比栈顶操作符的栈内优先级高，则直接将该操作符入栈
        3.2.如果取到的操作符栈外优先级比栈顶元素栈内优先级低，则将栈顶元素压到后序列表中，再将该操作符与栈顶元素
        进行比较，如果栈顶元素栈内优先级低，则继续压到后序列表中，直到不满足条件，这时判断如果该操作符是右括号，
        那么将栈顶元素丢弃（此时的栈顶元素是左括号），并丢弃该操作符，取下一个操作符。如果该操作符不是右括号，
        则将该操作符压入到栈顶。
        3.3.如果取到的操作符栈外优先级和栈顶元素栈内优先级相同，则丢弃栈顶操作符。
        （PS:这种情况很少出现，只有在括号匹配出现的时候）
    4.最后将栈中剩余的其他操作符顺序反转之后丢弃之前存入的#操作符，之后追加到后序表达式列表中。
这样最后生成的就是一个后序表达式列表，再将替换出来的操作数替换到后序表达式列表中，真正完成了后序表达式列表的生成。
"""


def postfix_expression(expression, num_list):
    postfix_list, stack = [], []  # 定义后序表达式列表以及操作符栈
    stack.append("#")  # 先在栈底压入操作符#(PS:因为#操作符的优先级最低，不会被退出栈)
    for char in expression:  # 遍历表达式
        if char not in isp:  # 获取到的字符是操作数占位符，则将操作数占位符直接压到后序表达式列表中
            postfix_list.append(char)
        elif isp[stack[-1]] < icp[char]:  # 如果栈顶元素栈内优先级比操作符栈外优先级低，将操作符压入栈中
            stack.append(char)
        elif isp[stack[-1]] > icp[char]:  # 如果栈顶元素栈内优先级比操作符栈外优先级高
            while isp[stack[-1]] > icp[char]:  # 将栈顶元素循环追加到后序表达式列表中，直到不满足条件
                postfix_list.append(stack.pop())
            if char == ")":  # 如果操作符是右括号，则不满足条件时栈顶元素肯定是左括号，丢弃栈顶元素及该操作符，取下一个字符
                stack.pop()
                continue
            stack.append(char)  # 否则将该操作符压入栈中
        else:
            stack.pop()  # 如果操作操作符栈外优先级和栈顶元素栈内优先级相同，则丢弃栈顶元素，获取下一个字符(在优先级表中只有括号的栈外优先级和站内优先级存在相等情况)
    stack.reverse()  # 将栈中剩余操作符反转
    stack.pop()  # 丢弃之前存入的#操作符
    postfix_list.extend([i for i in stack])  # 将反转并丢弃#操作符的站内操作符全部追加到后序表达式列表中
    num_list.reverse()  # 将操作数列表反转
    postfix_list = [num_list.pop() if i == "S" else i for i in postfix_list]  # 将翻转后的操作数列表通过pop方式替换后序表达式中的操作数占位符
    return postfix_list  # 将生成的真正的后序表达式列表返回


"""计算四则运算函数，传入后序表达式列表，使用一个栈保存计算结果，从左到右读取后序表达式列表，如果碰到操作符，
将操作符及其前面的两个操作数取出，进行计算，将计算的中间结果重新压入栈中，这样，遍历完后序表达式列表之后，栈中
存下的就是最后的计算结果了，将计算结果返回给调用函数。"""


def caculate_result(postfix_list):
    stack = []  # 定义存储中间计算结果的栈
    for i in postfix_list:  # 遍历后序表达式列表
        stack.append(i)  # 将后序表达式中的元素压到栈顶
        if i == "+":  # 假如得到的操作符是+号，将刚压入到栈顶的+丢弃，并取出其前面两个操作数，相加，将得到的中间计算结果再压入栈中
            stack.pop()
            right, left = stack.pop(), stack.pop()
            stack.append(left + right)
        elif i == "-":  # 假如得到的操作符是-号，将刚压入到栈顶的-丢弃，并取出其前面两个操作数，相减，将得到的中间计算结果再压入栈中
            stack.pop()
            right, left = stack.pop(), stack.pop()
            stack.append(left - right)
        elif i == "*":  # 假如得到的操作符是*号，将刚压入到栈顶的*丢弃，并取出其前面两个操作数，相乘，将得到的中间计算结果再压入栈中
            stack.pop()
            right, left = stack.pop(), stack.pop()
            stack.append(left * right)
        elif i == "/":  # 假如得到的操作符是/号，将刚压入到栈顶的/丢弃，并取出其前面两个操作数，相除，将得到的中间计算结果再压入栈中，注意这时候要判断除数为0的情况
            stack.pop()
            right, left = stack.pop(), stack.pop()
            if right != 0:  # 如果除数不为0，则按照正常操作计算
                stack.append(left / right)
            else:  # 否则，爆出错误，并将返回值置为false，程序结束
                print("除数不能为0...")
                return "false"
    return stack[0]  # 计算完成之后，栈中就只剩下一个元素了，这个元素就是最终得到的计算结果。


"""主调函数，获取到表达式之后，先对表达式进行合法性检查，通过之后，再将表达式替换成字符占位表达式和操作数列表，
之后再将获取到的内容通过调用后序表达式生成函数生成后序表达式，再调用计算函数计算最终结果。"""


@show_time  # 装饰器函数，计算该计算过程花费的时间
def main():
    expression = "1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10.5 * 568/14 )) - " \
                 "(-4*3)/ (16-3*2) )".strip().replace(" ", "")
    expression="1 - 2 * ((60-30 +(-40/20) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/(16-3*2))".strip().replace(" ","")
    if checkout(expression):  # 表达式合法化检查通过
        new_expression, num_list = replace_expression(expression)  # 调用表达式替换函数
        postfix_list = postfix_expression(new_expression, num_list)  # 调用后序表达式列表生成函数
        result = caculate_result(postfix_list)  # 调用计算函数获取最终结果
        if result == "false":  # 如果除数为0的话，打印错误，并结束程序
            print("表达式逻辑错误，即将退出...")
        else:  # 否则打印计算结果以及调用eval内置方法计算表达式结果，对比两种计算方式结果是否一致。
            print("计算结果:%s" % result)
            print("eval计算结果:%s" % eval(expression))
    else:
        print("本程序即将退出...")  # 表达式未通过合法化检查，退出程序


if __name__ == "__main__":  # 内部测试函数
    main()
