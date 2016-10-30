#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-17
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from module import actions
from module import auth
from module import logger
from conf import settings
atm_log=logger.logger("ATM_LOG")

@auth.atm_auth_log(atm_log)
def pay_money(payment,shop_card):  # 支付
    card_log=logger.logger(auth.atm_auth_card_id)
    business_log=logger.logger(shop_card)
    operation_result=actions.__operation_money__(payment,"consume",auth.atm_auth_card_id)
    if operation_result[0]:
        print("用户:%s支付成功!本次扣款:%s RMB!Interest %s RMB!"%(auth.atm_auth_card_id,operation_result[1],operation_result[1]-payment))
        card_log.info("Card:%s pay %s RMB to shop sucessful!Interest %s RMB!"%(auth.atm_auth_card_id,payment,operation_result[1]-payment))
        atm_log.info("Card:%s pay %s RMB to shop sucessful!Interest %s RMB!"%(auth.atm_auth_card_id,payment,operation_result[1]-payment))
        actions.__operation_money__(payment,"repay",shop_card)
        business_log.info("Business Card:%s receive Card:%s %s RMB for shopping successful!"%(shop_card,auth.atm_auth_card_id,payment))
        auth.atm_auth_flag = False
        auth.atm_auth_admin = False
        auth.atm_auth_card_id = ""
        return True
    else:
        print("抱歉，您的信用卡:%s余额不足..."%(auth.atm_auth_card_id))
        card_log.info("Card:%s pay %s RMB to shop failed!Don't have enough money!"%(auth.atm_auth_card_id,payment))
        atm_log.info("Card:%s pay %s RMB to shop failed!Don't have enough money!"%(auth.atm_auth_card_id,payment))
        auth.atm_auth_flag = False
        auth.atm_auth_admin = False
        auth.atm_auth_card_id = ""
        return False
