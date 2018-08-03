#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: zip_file.py
@time: 2018/4/17 9:27
"""
import os, os.path
import zipfile

# 压缩函数
def zip_dir(file_path, zfile_path):
    '''
    function: 压缩
    :param file_path: 要压缩的文件路径，可以是文件夹
    :param zfile_path: 存放压缩文件的路径
    :return:
    '''
    filelist = []
    if os.path.isfile(file_path):
        filelist.append(file_path)
    else:
        for root, dirs, files in os.walk(file_path):
            for name in files:
                filelist.append(os.path.join(root, name))
                print('joined:', os.path.join(root, name), dirs)

    zf = zipfile.ZipFile(zfile_path, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(file_path):]
        print(arcname, tar)
        zf.write(tar, arcname)
    zf.close()

def main():
    file_path = input("The file_path is:")
    zfile_path = input("The zfile_path is:")
    zip_dir(file_path, zfile_path)
    # zip_dir(r'/tmp/xungou', r'/tmp/xungou.zip')

if __name__ == '__main__':
    main()