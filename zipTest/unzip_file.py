#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: unzip_file.py
@time: 2018/4/17 10:21
"""
import zipfile
import os, os.path

def unzip_dir(zfile_path, unzfile_path):
    '''
    function: 解压
    :param zfile_path: 压缩文件路径
    :param unzfile_path: 解压缩路径
    :return:
    '''
    try:
        with zipfile.ZipFile(zfile_path) as zfile:
            zfile.extractall(path=unzfile_path)
    except zipfile.BadZipFile as e:
        print(zfile_path + 'is a bad zip file, please check!')

def main():
    zfile_path = input("The zfile_path is:")
    unzfile_path = input("The unzfile_path is:")
    unzip_dir(zfile_path, unzfile_path)

if __name__ == '__main__':
    main()