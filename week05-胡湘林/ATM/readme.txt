ATM
  ├─ATM
  │  │
  │  ├─bin  # ATM的执行入口目录
  │  │     atm.py  # ATM的执行入口文件
  │  │
  │  ├─conf  # ATM的配置文件目录
  │  │     settings.py  # ATM的配置文件
  │  │
  │  ├─data  # ATM的数据存放目录
  │  │  └─users_info  # ATM的用户数据存放目录
  │  │          123456  # CARD ID 为123456的用户数据文件
  │  │          666666
  │  │
  │  ├─logs  # ATM的日志文件目录
  │  │      123456  # CARD ID 为123456的用户操作日志
  │  │      666666
  │  │      ATM_LOG  # ATM的操作日志文件
  │  │
  │  ├─module  # 各种模块目录
  │        actions.py  # 存放 转账，提现，还款，密码加密，操作等函数
  │        admin.py  # 存放 管理员相关操作函数，包含：管理主函数，对用户的曾，删，改，查函数，修改密码函数，解除锁定函数
  │        auth.py  # 存放认证装饰器函数
  │        db_handler.py  # 存放链接数据操作函数，所有其他函数需要访问数据都需要调用这个文件提供的接口
  │        logger.py  # 存放日志定义函数
  │        main.py  # ATM模块的功能主入口
  │        trans_action.py  # 支付模块，为了给shop调用的
  │
  ├─bin  # 整个程序主入口目录
  │      bin.py  # 整个程序的主入口文件
  │
  └─shop
      │
      ├─shop_bin  # 商城模块的主入口目录
      │     shop.py  # 商城模块的主入口文件
      │
      ├─shop_conf  # 商城模块的配置文件目录
      │     settings.py  # 商城模块的配置文件
      │   
      │
      ├─shop_data  # 商城模块的数据存放目录
      │  │  goods_data.json  # 存放商城中的商品
      │  │
      │  └─users_info  # 存放商城用户数据目录
      │          123456
      │          654321
      │
      ├─shop_logs  # 存放商城日志文件目录
      │      123456  # 用户ID为123456的用户的操作日志
      │      shop_log  # 整个商城的操作日志
      │
      ├─shop_module  # 商城各种功能模块目录
            admin.py  # 管理模块，涉及管理主函数，对用户的曾，删，改，查函数，修改密码函数，解除锁定函数
            auth.py  # 认证装饰器模块
            db_handler.py  # 存放链接数据操作函数，所有其他函数需要访问数据都需要调用这个文件提供的接口
            encry_passwd.py  # 加密密码模块，所有密码都是密文存储的，在存储到文件之前都需要调用这个模块对密码进行hash
            goods_show.py  # 商品展示模块
            logger.py  # 日志模块
            main.py  # 各种功能模块的主入口
            shop_cart.py  # 购物车模块，包含结账和删除商品函数，其中结账函数执行时会调用ATM中的traction_action模块结账