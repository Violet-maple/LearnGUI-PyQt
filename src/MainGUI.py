#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

import qtawesome
from PyQt5.QtCore import QSize, Qt, pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtWidgets import (QWidget, QMainWindow, QGridLayout,
                             QPushButton, QLabel, QLineEdit,
                             QToolButton, QProgressBar, QApplication,
                             QDesktopWidget)


class MainUi(QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        self.row = 5
        self.column = 10
        self.init_ui()
    
    def init_ui(self):
        self.setWindowIcon(QIcon('./img/index.ico'))
        self.setWindowTitle("工具")
        # self.setFixedSize(960, 700)
        self.resize(960, 700)
        # self._center()
        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_layout = QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        
        # 创建上侧部件
        self.up_widget = QWidget()
        self.up_widget.setObjectName('up_widget')
        self.up_layout = QGridLayout()
        self.up_widget.setLayout(self.up_layout)
        
        # 创建中侧部件
        self.mid_widget = QWidget()
        self.mid_widget.setObjectName('mid_widget')
        self.mid_layout = QGridLayout()
        self.mid_widget.setLayout(self.mid_layout)
        
        # 创建下侧部件
        self.down_widget = QWidget()
        self.down_widget.setObjectName('down_widget')
        self.down_layout = QGridLayout()
        self.down_widget.setLayout(self.down_layout)
        
        self.main_layout.addWidget(self.up_widget, 0, 0, 1, 9)
        self.main_layout.addWidget(self.mid_widget, 1, 0, 1, 8)
        self.main_layout.addWidget(self.down_widget, 2, self.column - 2, self.row, 1)
        self.setCentralWidget(self.main_widget)
        
        # 创建头部（head）
        self.head_widget = QWidget()
        self.head_layout = QGridLayout()
        self.head_widget.setLayout(self.head_layout)
        
        name = 'name'
        for i in range(10):
            self.tool_btn = QToolButton()
            self.tool_btn.setText(f"{name}_{i}")  # 设置按钮文本
            self.tool_btn.setIcon(QIcon('./img/index.ico'))  # 设置按钮图标
            self.tool_btn.setIconSize(QSize(50, 50))  # 设置图标大小
            self.tool_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            
            self.head_layout.addWidget(self.tool_btn, 0, i)
        
        self.up_layout.addWidget(self.head_widget, 0, 0, 0, 0)
        
        # 创建中部（middle）
        self.middle_widget = QWidget()
        self.middle_layout = QGridLayout()
        self.middle_widget.setLayout(self.middle_layout)
        
        for i in range(self.row):
            self.none = QLabel("  ")
            self.middle_icon = QLabel(chr(0xf002) + f'目录_{i}:')
            self.middle_icon.setFont(qtawesome.font('fa', 12))
            self.middle_input = QLineEdit()
            self.middle_input.setPlaceholderText("请选择文件...")
            self.middle_btn = QPushButton(qtawesome.icon('fa.film', color='green'), "选择文件")
            self.middle_btn.setObjectName(f'middle_btn_{i}')
            
            self.middle_layout.addWidget(self.none, i, 0, 1, 1)
            self.middle_layout.addWidget(self.middle_icon, i, 1, 1, 1)
            self.middle_layout.addWidget(self.middle_input, i, 2, 1, 4)
            self.middle_layout.addWidget(self.middle_btn, i, 5, 1, 1)
        
        self.mid_layout.addWidget(self.middle_widget, 0, 0, 1, 1)
        
        # 创建尾部
        self.tail_widget = QWidget()
        self.tail_layout = QGridLayout()
        self.tail_widget.setLayout(self.tail_layout)
        
        self.tail_btn = QPushButton(qtawesome.icon('fa.download', color='green'), "运行")
        self.tail_layout.addWidget(self.tail_btn, 0, 9, 1, 1)
        self.down_layout.addWidget(self.tail_widget, 0, 0, 0, 0)
        self.set_style()
        
        # self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
    
    def set_style(self):
        self.up_widget.setStyleSheet("""
            #up_widget{background:gray;}
        """)
        self.mid_widget.setStyleSheet("""
            #mid_widget{background:darkGray;}
        """)
        self.down_widget.setStyleSheet("""
            #down_widget{background:darkGray;}
        """)
        self.head_widget.setStyleSheet("""
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
        """)
        self.middle_widget.setStyleSheet("""
            QLineEdit{
                border:1px solid gray;
                border-radius:10px;
                padding:5px 2px;
            }
            QPushButton{
                border:none;
                border-right:1px gray;
                border-radius:10px;
                width:40%;
                padding:5px 2px;
            }
            QPushButton:hover{
                color:red;font-weight: bold;
            }
            QLabel{
                padding:0 0 0 100%;
            }
        """)
        self.tail_widget.setStyleSheet("""
            QPushButton{
                border:none;
                border-right:1px gray;
                border-radius:10px;
                padding:5px 2px;
            }
            QPushButton:hover{
                color:red;font-weight: bold;
            }
        """)
    
    def paintEvent(self, event):
        # 设置背景颜色
        painter = QPainter(self)
        background_color = QColor()
        background_color.setNamedColor('darkGray')
        painter.setBrush(background_color)
        painter.drawRect(self.rect())
    
    # def _center(self):
    #     # 窗口居中
    #     screen = QDesktopWidget().screenGeometry()
    #     size = self.geometry()
    #     self.move((screen.width() - size.width()) / 2,
    #               (screen.height() - size.height()) / 2)


def main():
    app = QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
