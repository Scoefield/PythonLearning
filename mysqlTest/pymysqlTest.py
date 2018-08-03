#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: pymysqlTest.py
@time: 2018/4/19 17:12
"""
import pymysql

def main():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='dys123', database='managerie', charset='utf8')
    cur = conn.cursor()
    sql = "select * from person"
    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        print(result)


if __name__ == '__main__':
    main()