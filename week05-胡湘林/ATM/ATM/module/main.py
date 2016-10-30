#!/usr/bin/env python
# encoding:utf-8
# __author__: huxianglin
# date: 2016-09-14
# blog: http://huxianglin.cnblogs.com/ http://xianglinhu.blog.51cto.com/

from module import auth
from module import admin
from module import actions
from module import logger

atm_log=logger.logger("ATM_LOG")

@auth.atm_auth_log(atm_log)
def main():  # 主菜单
    current_card_log=logger.logger(auth.atm_auth_card_id)
    admin_operation = {"转账": actions.transfer_accounts,
                       "提现": actions.withdraw,
                       "还款": actions.repay_money,
                       "管理": admin.admin}
    user_operation = {"转账": actions.transfer_accounts, "提现": actions.withdraw, "还款": actions.repay_money}
    while True:
        if auth.atm_auth_flag and auth.atm_auth_admin:
            operation_flag = actions.operations(admin_operation,atm_log,current_card_log)
            if not operation_flag:
                auth.atm_auth_flag = False
                auth.atm_auth_admin = False
                auth.atm_auth_card_id = ""
                break
        elif auth.atm_auth_flag:
            operation_flag = actions.operations(user_operation,atm_log)
            if not operation_flag:
                auth.atm_auth_flag = False
                auth.atm_auth_admin = False
                auth.atm_auth_card_id = ""
                break

if __name__ == "__main__":
    main()
