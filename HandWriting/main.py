#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: main.py
@time: 2018/4/16 14:03
"""
import sys
from PyQt5.QtWidgets import QApplication
from Learning import Learning

if __name__ == '__main__':
    app = QApplication(sys.argv)

    py_learning = Learning()
    py_learning.show()

    sys.exit(app.exec_())
