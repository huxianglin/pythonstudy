# 用户信息管理系统

## 本节内容
1. 作业需求
2. 表结构设计
3. 代码模块设计

## 1.作业需求

    作业：
        参考表结构：
            用户类型

            用户信息

            权限

            用户类型&权限
        功能：

            # 登陆、注册、找回密码
            # 用户管理
            # 用户类型
            # 权限管理
            # 分配权限

        特别的：程序仅一个可执行文件

## 2.表结构设计
本系统在设计表结构时，设计了两张表，一张是userinfo表，另一张是privileges表。建表语句如下：

    CREATE table userinfo(
    	uid int auto_increment PRIMARY KEY,
    	username varchar(64) NOT NULL,
    	pwd char(41) NOT NULL,
    	email varchar(128) NOT NULL,
    	privilege_id int NOT NULL
    ) ENGINE = INNODB DEFAULT charset="utf8";
    
    CREATE TABLE privileges (
    	pid INT auto_increment PRIMARY KEY,
    	pname VARCHAR (64) NOT NULL,
    	plist set (
    		"show_local",
    		"show_all",
    		"update_user"
    	) NOT NULL DEFAULT "show_local"
    ) ENGINE = INNODB DEFAULT charset = "utf8";
    
    ALTER TABLE userinfo ADD CONSTRAINT fk_u_p FOREIGN KEY userinfo (privilege_id) REFERENCES privileges (pid);

userinfo表通过fk_u_p外键关联privileges表，设计权限树部分，在privileges表中的plist字段，使用set类型来存储权限列表。这里面目前只涉及到了两种用户，admin用户和普通用户，admin用户拥有set里面所有的字段，而普通用户只拥有show_local字段。

- admin 权限：查看所有用户,给用户更改分配权限,查看当前用户信息
- user 权限：查看当前用户信息

权限相关设置sql如下：

    insert into privileges(pname,plist) values("user","show_local");
    insert into privileges(pname,plist) values("admin",'show_local,show_all,update_user');

这样设计之后，在之后程序中拿到用户信息之后，可以通过该字段的字符串使用反射/自省直接去对象中执行相应的方法。

## 3.代码模块设计

代码中主要涉及到两个类，一个类是Exec_db类，被设计为单例模式，里面使用了连接池，可以与数据库创建多个连接。该类内部的一些方法是对数据库的一些操作的抽象和封装，这样，外部想要执行sql语句只需要构建好sql语句和相应数据就可以调用相应的方法去执行。

另一个类是useroperation类，这个类中封装了所有与数据库操作相关的sql，所有操作数据库的操作都需要通过这个类来实现。包括之前在设计表结构时在privileges表中的plist字段里面的内容字符串，就是通过反射/自省来调用该类中的相应方法实现。

另一个实现模块是login装饰器，该装饰器中封装了三个操作，1登录，2注册，3修改密码，这三个操作通过调用不同的函数实现，其中涉及到数据库操作是通过调用useroperation类中的静态方法实现（因为这三个操作时，用户还没登陆，所以没有创建相应的对象，所以相关方法使用静态方法实现。）