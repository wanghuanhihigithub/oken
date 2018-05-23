# -*- coding: utf-8 -*-
#导入MYSQL驱动
import mysql.connector
conn = mysql.connector.connect(user='root',password='',database='test')
cursor = conn.cursor()

#创建user表
cursor.execute('create table user(id varchar(20) primary key, name varchar(20))')
#插入一行记录
cursor.execute('insert into user(id,name) values(%s,%s)',['1', 'Michael'])
cursor.rowcount
conn.commit()

cursor = conn.cursor()
cursor.execute('select * from user where id = %s',('1',))
values = cursor.fetchall()
print(values)
cursor.close()
conn.close()