#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-17
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import hashlib
from module import db_handler
from module import auth
from conf import settings
from module import logger
from module import auth

def encry_passwd(passwd):
    sha256_obj = hashlib.sha256()
    sha256_obj.update(passwd.encode("utf-8"))
    return sha256_obj.hexdigest()


def operations(operations,atm_log,current_card_log=False):
    num_of_operation = []
    print("您支持的操作如下".center(50, "*"))
    for i, j in enumerate(sorted(operations), 1):
        print(i, j, "\t", end="")
        num_of_operation.append(j)
    print()
    operation = input("请输入您的操作:").strip()
    if operation in operations or operation.isdigit():
        if operation.isdigit():
            operation = int(operation)
            if 1 <= operation <= len(operations):
                operation = num_of_operation[operation - 1]
            else:
                print("抱歉，您输入的操作不在本系统中...")
                return True
        for i in operations:
            if operation == i:
                if operation in ["转账","提现","还款"]:
                    operations[i](atm_log,current_card_log)
                else:
                    operations[i](atm_log)
        return True
    elif operation in["q","b"]:
        return False
    else:
        print("抱歉，您输入的操作不在本系统中...")
        return True


def __operation_money__(oper_money,operation,card_id,*args):
    operations=settings.TRANSACTION_TYPE
    if operation in operations:
        current_data=db_handler.read_data(card_id)
        if operations[operation]["action"] == "minus":  # 扣钱
            new_oper_money=oper_money*(1+operations[operation]["interest"])
            if current_data["balance"]-new_oper_money>current_data["limit"]*-1:
                current_data["balance"]-=new_oper_money
                db_handler.write_data(card_id,current_data)
                return True,new_oper_money,current_data["balance"]
            else:
                print("余额不足...")
                return False,None,None
        elif operations[operation]["action"] == "plus":  # 存钱
            new_oper_money=oper_money*(1+operations[operation]["interest"])
            current_data["balance"]+=new_oper_money
            db_handler.write_data(card_id,current_data)
            return True,new_oper_money,current_data["balance"]


def transfer_accounts(atm_log,current_card_log):  # 转账
    peer_card_id = input("请输入你要转账的账户:").strip()
    if peer_card_id in auth.ATM_CARD_LIST:
        transfer_money = input("请输入您要转账的金额:").strip()
        if transfer_money.isdigit():
            transfer_money = int(transfer_money)
            atm_log.debug("Card:%s wangt to transfer %s to Card:%s"%(auth.atm_auth_card_id,transfer_money,peer_card_id))
            operation_result=__operation_money__(transfer_money,"transfer",auth.atm_auth_card_id)
            if operation_result[0]:
                current_card_log.info("Card:%s transfer %s to Card:%s Successful!transfer interest %s RMB!"%(auth.atm_auth_card_id,transfer_money,peer_card_id,operation_result[1]-transfer_money))
                atm_log.info("Card:%s transfer %s to Card:%s successful!"%(auth.atm_auth_card_id,transfer_money,peer_card_id))
                print("转账成功！您本次转账:%s元，利息:%s 余额:%s元!" % (transfer_money,operation_result[1]-transfer_money,operation_result[2]))
                __operation_money__(transfer_money,"repay",peer_card_id)
                peer_card_log=logger.logger(peer_card_id)
                peer_card_log.info("From Card:%s Receive %s RMB!"%(auth.atm_auth_card_id,transfer_money))
            else:
                print("抱歉，您的余额不足...")
                atm_log.warning("Card:%s transfer %s to Card:%s failed!Not enough money!"%(auth.atm_auth_card_id,transfer_money,peer_card_id))
        else:
            print("抱歉，您输入的金额不合法...")
    else:
        print("抱歉，对方卡号不存在...")


def withdraw(atm_log,current_card_log):  # 提现
    withdraw_money = input("请输入您要提现的金额:")
    if withdraw_money.isdigit():
        withdraw_money = int(withdraw_money)
        atm_log.info("Card:%s want to withdraw %s RMB!"%(auth.atm_auth_card_id,withdraw_money))
        operation_result=__operation_money__(withdraw_money,"withdraw",auth.atm_auth_card_id)
        if operation_result[0]:
            print("提现成功！您本次提现:%s元，利息:%s元,当前可用余额:%s元" % (withdraw_money,operation_result[1]-withdraw_money,operation_result[2]))
            atm_log.info("Card:%s withdraw %s successful!"%(auth.atm_auth_card_id,withdraw_money))
            current_card_log.info("Card:%s withdraw %s RMB interest %s RMB!"%(auth.atm_auth_card_id,withdraw_money,operation_result[1]-withdraw_money))
        else:
            print("抱歉，您的余额不足...")
            atm_log.warning("Card:%s withdraw %s failed!Not enough money!"%(auth.atm_auth_card_id,withdraw_money))
    else:
        print("抱歉，您的输入不合法...")


def repay_money(atm_log,current_card_log):  # 还款
    repayment_money = input("请输入您要还款的金额:")
    if repayment_money.isdigit():
        repayment_money = int(repayment_money)
        atm_log.info("Card:%s want to repay %s"%(auth.atm_auth_card_id,repayment_money))
        operation_result=__operation_money__(repayment_money,"repay",auth.atm_auth_card_id)
        print("还款成功！您本次还款:%s元，当前可用余额:%s元" % (repayment_money, operation_result[2]))
        atm_log.info("Card:%s repay %s successful!"%(auth.atm_auth_card_id,repayment_money))
        current_card_log.info("Card:%s repay %s RMB!"%(auth.atm_auth_card_id,repayment_money))
    else:
        print("抱歉，您的输入不合法...")
