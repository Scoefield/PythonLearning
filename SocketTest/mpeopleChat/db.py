#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: db.py
@time: 2018/4/20 13:41
"""
import json

# 创建一个类，代替数据库
class DB(object):
    def __init__(self, path='Storage.db'):
        self.path = path

    def get_data(self, data=None):
        try:
            with open(self.path) as f:
                data = json.load(f)
        except IOError as e:
            return data # 首次取数据时，由于文件不存在或没数据，将返回默认值 None
        finally:
            return data

    def put_data(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f)
