#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: sqltest.py
@time: 2018/6/20 9:48
"""
import pymysql

para = []
with open('sql.conf', 'r') as f:
    para = f.read().replace('\n', '=').split('=')
print(para)
apphost = '{}'.format(para[1])
appdbname = '{}'.format(para[3])
appuser = '{}'.format(para[5])
apppasswd = '{}'.format(para[7])
appport = 3306

def sqlConnect():
    conn = pymysql.connect(host=apphost, user=appuser, passwd=apppasswd, db=appdbname, port=appport, charset='utf8')
    return conn

if __name__ == '__main__':
    try:
        conn = sqlConnect()
        cur = conn.cursor()
        sql = "SELECT itemno,modeltext FROM AI_item where paperid=1 and itemtype='read'"
        cur.execute(sql)
        results = cur.fetchall()

        cur.close()
        conn.close()
        print(results)
    except Exception :
        print("except")
