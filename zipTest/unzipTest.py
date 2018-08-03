#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: unzipTest.py
@time: 2018/6/21 16:15
"""
import zipfile
import os, os.path

def unzipFunction(zip_file, unzippath):
    try:
        with zipfile.ZipFile(zip_file) as zfile:
            zfile.extractall(path=unzippath)
    except:
        print("unzipfile fail...")

if __name__ == '__main__':
    zip_file = 'include.zip'
    unzippath = 'include'
    unzipFunction(zip_file, unzippath)
