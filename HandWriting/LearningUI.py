#! /usr/bin/env python
# encoding:utf-8
"""
@author: DYS
@file: LearningUI.py
@time: 2018/4/16 11:43
"""
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QComboBox, QDesktopWidget, QApplication)
from PyQt5.QtGui import (QPainter, QPen, QFont)
from PyQt5.QtCore import Qt
import sys

class LearningUI(QWidget):

    def __init__(self):
        super(LearningUI, self).__init__()

        self.__init_ui()

        # 设置只有鼠标按下时才跟踪移动，否则不按的时候也在画画
        self.setMouseTracking(False)
        # self.pos_xy保存所有绘画的点
        self.pos_xy = []
        # 设置pos_x、pos_y方便计算
        self.pos_x = []
        self.pos_y = []

        # 设置关联事件
        self.btn_learn.clicked.connect(self.btn_learn_on_clicked)   # 学习
        self.btn_recognize.clicked.connect(self.btn_recognize_on_clicked)   # 识别
        self.btn_clear.clicked.connect(self.btn_clear_on_clicked)   # 清屏

    def __init_ui(self):
        '''
         定义UI界面：
         三个按钮：学习、识别、清屏
         btn_learn、btn_recognize、btn_clear
         一个组合框：选择0-9
         combo_table
         两条标签：请在屏幕空白处用鼠标输入0-9中的某一个数字进行识别！
         一条输出识别结果的标签
         label_output
        '''

        # 添加三个按钮，分别是学习、识别、清屏
        self.btn_learn = QPushButton("学习", self)
        self.btn_learn.setGeometry(50, 400, 70, 40)
        self.btn_recognize = QPushButton("识别", self)
        self.btn_recognize.setGeometry(320, 400, 70, 40)
        self.btn_clear = QPushButton("清屏", self)
        self.btn_clear.setGeometry(420, 400, 70, 40)

        # 添加一个组合框，选择0-9
        self.combo_table = QComboBox(self)
        for i in range(10):
            self.combo_table.addItem("%d" % i)
        self.combo_table.setGeometry(150, 400, 70, 40)

        # 添加两条标签
        self.label_head = QLabel('请在屏幕空白处用鼠标输入0-9中的某一个数字进行识别！', self)
        self.label_head.move(75, 50)
        self.label_end = QLabel('2018/4/21 by Scoefield', self)
        self.label_end.move(375, 470)

        # 添加一条输出识别结果的标签
        '''
        setStyleSheet设置边框大小、颜色
        setFont设置字体大小、形状、加粗
        setAlignment设置文本居中
        '''
        self.label_output = QLabel('', self)
        self.label_output.setGeometry(50, 100, 150, 250)
        self.label_output.setStyleSheet("QLabel{border:1px solid black;}")
        self.label_output.setFont(QFont("Roman times", 100, QFont.Bold))
        self.label_output.setAlignment(Qt.AlignCenter)

        '''
        setFixedSize()固定了窗体的宽度与高度
        self.center()将窗体居中显示
        setWindowTitle()设置窗体的标题
        '''
        self.setFixedSize(550, 500)
        self.center()
        self.setWindowTitle('0-9手写体简单识别(机器学习中的"HelloWorld!")')

    def center(self):
        '''
         窗口居中显示
        '''
        qt_center = self.frameGeometry()
        desktop_center = QDesktopWidget().availableGeometry().center()
        qt_center.moveCenter(desktop_center)
        self.move(qt_center.topLeft())

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.blue, 2, Qt.SolidLine)
        painter.setPen(pen)

        '''
         首先判断pos_xy列表中是不是至少有两个点了
         然后将pos_xy中第一个点赋值给point_start
         利用中间变量pos_tmp遍历整个pos_xy列表
          point_end = pos_tmp

          判断point_end是否是断点，如果是
           point_start赋值为断点
           continue
          判断point_start是否是断点，如果是
           point_start赋值为point_end
           continue

          画point_start到point_end之间的线
          point_start = point_end
         这样，不断地将相邻两个点之间画线，就能留下鼠标移动轨迹了
        '''
        if len(self.pos_xy) > 1:
            point_start = self.pos_xy[0]
            for pos_tmp in self.pos_xy:
                point_end = pos_tmp

                if point_end == (-1, -1):
                    point_start = (-1, -1)
                    continue
                if point_start == (-1, -1):
                    point_start = point_end
                    continue

                painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
                point_start = point_end
        painter.end()

    def mouseReleaseEvent(self, event):
        '''
         重写鼠标按住后松开的事件
         在每次松开后向pos_xy列表中添加一个断点(-1, -1)
         然后在绘画时判断一下是不是断点就行了
         是断点的话就跳过去，不与之前的连续
        '''

        pos_test = (-1, -1)
        self.pos_xy.append(pos_test)

        self.update()

    def mouseMoveEvent(self, event):
        '''
         按住鼠标移动：将移动的点加入self.pos_xy列表
        '''

        # self.pos_x和self.pos_y总是比self.pos_xy少一到两个点，还不知道原因在哪
        self.pos_x.append(event.pos().x())
        self.pos_y.append(event.pos().y())

        # 中间变量pos_tmp提取当前点
        pos_tmp = (event.pos().x(), event.pos().y())
        # pos_tmp添加到self.pos_xy中
        self.pos_xy.append(pos_tmp)

        self.update()

    def btn_learn_on_clicked(self):
        '''
         需要用到数据库，因此在在子类中实现
        '''
        pass

    def btn_recognize_on_clicked(self):
        '''
         需要用到数据库，因此在在子类中实现
        '''
        pass

    def btn_clear_on_clicked(self):
        '''
         按下清屏按钮：
         将列表赋值为空
         将输出识别结果的标签赋值为空
         然后刷新界面，重新绘画即可清屏
        '''

        self.pos_xy = []
        self.pos_x = []
        self.pos_y = []
        self.label_output.setText('')
        self.update()

    def get_pos_xy(self):
        '''
         将手写体在平面上分为9个格子
         计算每个格子里点的数量
         然后点的数量转化为占总点数的百分比
         接着返回一个数组dim[9]
         横轴依次是min_x、min2_x、max2_x、max_x
         纵轴依次是min_y、min2_y、max2_y、max_y
        '''

        if not self.pos_xy:
            return None

        pos_count = len(self.pos_x)
        max_x = max(self.pos_x)
        max_y = max(self.pos_y)
        min_x = min(self.pos_x)
        min_y = min(self.pos_y)
        dim = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        dis_x = (max_x - min_x) // 3
        dis_y = (max_y - min_y) // 3

        min2_x = min_x + dis_x
        min2_y = min_y + dis_y
        max2_x = max_x - dis_x
        max2_y = max_y - dis_y

        for i in range(len(self.pos_x)):
            if self.pos_y[i] >= min_y and self.pos_y[i] < min2_y:
                if self.pos_x[i] >= min_x and self.pos_x[i] < min2_x:
                    dim[0] += 1
                    continue
                if self.pos_x[i] >= min2_x and self.pos_x[i] < max2_x:
                    dim[1] += 1
                    continue
                if self.pos_x[i] >= max2_x and self.pos_x[i] <= max_x:
                    dim[2] += 1
                    continue
            elif self.pos_y[i] >= min2_y and self.pos_y[i] < max2_y:
                if self.pos_x[i] >= min_x and self.pos_x[i] < min2_x:
                    dim[3] += 1
                    continue
                if self.pos_x[i] >= min2_x and self.pos_x[i] < max2_x:
                    dim[4] += 1
                    continue
                if self.pos_x[i] >= max2_x and self.pos_x[i] <= max_x:
                    dim[5] += 1
                    continue
            elif self.pos_y[i] >= max2_y and self.pos_y[i] <= max_y:
                if self.pos_x[i] >= min_x and self.pos_x[i] < min2_x:
                    dim[6] += 1
                    continue
                if self.pos_x[i] >= min2_x and self.pos_x[i] < max2_x:
                    dim[7] += 1
                    continue
                if self.pos_x[i] >= max2_x and self.pos_x[i] <= max_x:
                    dim[8] += 1
                    continue
            else:
                pos_count -= 1
                continue
        # 将数量转化为所占百分比
        for num in dim:
            num = num * 100 // pos_count

        return dim


def main():
    app = QApplication(sys.argv)
    learnui = LearningUI()
    learnui.show()
    app.exec_()

if __name__ == '__main__':
    main()
