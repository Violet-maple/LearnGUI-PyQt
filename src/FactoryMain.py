#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

import qtawesome
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtWidgets import (QWidget, QMainWindow, QGridLayout,
                             QPushButton, QToolButton, QApplication,
                             QDesktopWidget, QScrollBar)

from MiddlePackages.BMain import ObjFactory
from Config.setting import load_info


class MainUi(QMainWindow):
    clicked_num = 0
    container = {}
    
    def __init__(self, info):
        super(MainUi, self).__init__()
        self.icon = [ico for ico in info]
        self.column = len(self.icon)
        self.num = 10  # 界面头部展示模块数量
        self.init_ui()
    
    def init_ui(self):
        self.setWindowIcon(QIcon('./img/index.ico'))
        self.setWindowTitle("工具")
        self.resize(960, 600)
        self.statusBar().show()
        self._center()
        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_layout = QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        
        # 创建上侧部件
        self.up_widget = QWidget()
        self.up_widget.setObjectName('up_widget')
        self.up_widget.setFixedHeight(80)
        self.up_layout = QGridLayout()
        self.up_widget.setLayout(self.up_layout)
        # 创建滚动条
        self.slide = QScrollBar(True)
        self.slide.setObjectName('slide_roll_bar')
        self.slide.setMaximum(self.column)
        self.slide.setMinimum(self.num)
        self.slide.valueChanged.connect(self._value_change)
        # 创建进度条
        self.notice_btn = QPushButton("Analysis")
        self.notice_btn.setFixedSize(150, 25)
        
        # 创建中侧部件
        self.mid_widget = QWidget()
        self.mid_widget.setObjectName('mid_widget')
        self.mid_widget.setFixedHeight(450)
        self.mid_layout = QGridLayout()
        self.mid_widget.setLayout(self.mid_layout)
        
        # 创建下侧部件
        self.down_widget = QWidget()
        self.down_widget.setObjectName('down_widget')
        self.down_layout = QGridLayout()
        self.down_widget.setLayout(self.down_layout)
        
        self.main_layout.addWidget(self.up_widget, 0, 0, 1, self.column)
        self.main_layout.addWidget(self.slide, 1, 0, 1, self.column)
        self.main_layout.addWidget(self.notice_btn, 2, 0, 1, 1)
        self.main_layout.addWidget(self.mid_widget, 3, 2, 1, self.column-2)
        self.main_layout.addWidget(self.down_widget, 4, self.column - 1, 1, 1)
        self.setCentralWidget(self.main_widget)
        
        # 创建头部（head）
        self.head_widget = QWidget()
        self.head_layout = QGridLayout()
        self.head_widget.setLayout(self.head_layout)
        
        self.load_model_ico(0, self.num) if self.num < self.column else self.load_model_ico(0, self.column)
        self.up_layout.addWidget(self.head_widget, 0, 0, 0, 0)
        # 创建中部
        
        # 创建尾部
        self.tail_widget = QWidget()
        self.tail_layout = QGridLayout()
        self.tail_widget.setLayout(self.tail_layout)
        
        self.tail_btn = QPushButton("Execute")
        self.tail_layout.addWidget(self.tail_btn, 0, 0, 1, 1)
        self.tail_btn.setFixedSize(70, 30)
        self.down_layout.addWidget(self.tail_widget, 0, 0, 0, 0)
        self.set_style()
        
        self.main_layout.setSpacing(0)
        # self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
            
    def _value_change(self):
        value = self.slide.value()
        start = value - self.num
        self.statusBar().showMessage(f'Current Value is {value}')
        self.del_layout(self.head_layout)
        self.load_model_ico(start, value)
        
    def load_model_ico(self, start, end):
        for i in range(start, end):
            self.tool_btn = QToolButton()
            self.tool_btn.setText(f"{self.icon[i]}")  # 设置按钮文本
            self.tool_btn.setObjectName(f"{self.icon[i]}")  # 设置按钮文本
            self.tool_btn.setFixedSize(80, 55)
            self.tool_btn.setIcon(qtawesome.icon(f'fa.{self.icon[i]}', color='white'))  # 设置按钮图标
            self.tool_btn.setIconSize(QSize(30, 30))  # 设置图标大小
            self.tool_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            self.tool_btn.clicked.connect(self._clicked)
        
            self.head_layout.addWidget(self.tool_btn, 0, i)
    
    def _clicked(self):
        model_name = self.sender().text()
        self.statusBar().showMessage(f'Current Value is {model_name}')
        self.change_style(model_name)
        self.del_layout(self.mid_layout)
        if ObjFactory.create(self, model_name):
            self.set_mid_style()
        else:
            self.set_mid_style(False)
            print("failed")
        self.show()
        
    @staticmethod
    def del_layout(layout):
        for i in range(layout.count()):
            layout.itemAt(i).widget().deleteLater()
    
    def change_style(self, text):
        self.head_widget.setStyleSheet("""
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
            #%s{
                border:2px dotted black;
                background:gray;
            }
        """ % text)
    
    def set_mid_style(self, flag=True):
        if flag:
            self.mid_widget.setStyleSheet("""
                #mid_widget{
                    background:white;
                    border-top-left-radius: 5px;
                    border-bottom-left-radius: 5px;
                }
            """)
        else:
            self.mid_widget.setStyleSheet("""
                #mid_widget{background:#009CAB;}
            """)
    
    def set_style(self):
        self.up_widget.setStyleSheet("""
            #up_widget{background:#006CAB;}
        """)
        self.down_widget.setStyleSheet("""
            #down_widget{background:#009CAB;}
        """)
        self.head_widget.setStyleSheet("""
            QToolButton{
                border:none;
            }
            QToolButton:hover{border-bottom:2px solid #F76677;}
        """)
       
        self.tail_widget.setStyleSheet("""
            QPushButton{
                background:green;
                font-size:16px;
                font-weight: bold;
                border-radius:2px;
            }
            QPushButton:hover{
                color:red;
            }
        """)
    
    def paintEvent(self, event):
        # 设置背景颜色
        painter = QPainter(self)
        background_color = QColor()
        background_color.setNamedColor('#009CAB')
        painter.setBrush(background_color)
        painter.drawRect(self.rect())
    
    def _center(self):
        # 窗口居中
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


def main():
    
    app = QApplication(sys.argv)
    gui = MainUi(load_info())
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
