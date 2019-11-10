#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import traceback
from time import sleep

from utils import const

import qtawesome
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QCalendarWidget

from utils.Style import set_first_mode_style
from MiddlePackages.ABCclass import MiddleWidget, GetDataError


class FourthMode(MiddleWidget):
    def __init__(self, obj, name):
        super().__init__(obj, name)
        self._thread = None
        self._obj = obj
        self.name = name
        self.row = 2
        self.set_up()
    
    def set_up(self):
        middle_widget = QWidget()
        self.middle_layout = QGridLayout()
        middle_widget.setLayout(self.middle_layout)
        for i in range(self.row):
            middle_icon = QLabel(chr(0xf002) + f'目录_{i}:')
            middle_icon.setFont(qtawesome.font('fa', 12))
            middle_icon.setFixedSize(50, self.height)
            middle_input = QLineEdit()
            middle_input.setFixedHeight(self.height)
            middle_input.setObjectName(f'middle_input_{i}')
            middle_btn = QPushButton("…")
            middle_btn.setFixedSize(50, self.height)
            middle_btn.setObjectName(f'middle_btn_{i}')
            middle_btn.setToolTip('点击选择文件')
            middle_btn.clicked.connect(lambda: self.open_file(middle_widget))
            
            self.middle_layout.addWidget(middle_icon, i, 0, 1, 1)
            self.middle_layout.addWidget(middle_input, i, 1, 1, self.row - 1)
            self.middle_layout.addWidget(middle_btn, i, self.row, 1, 1)
        
        middle_icon = QLabel(chr(0xf002) + f'目录_{i}:')
        middle_icon.setFont(qtawesome.font('fa', 12))
        middle_icon.setFixedSize(50, self.height)
        
        self.middle_time = QLineEdit()
        self.middle_time.setFixedHeight(self.height)
        self.middle_time.setObjectName(f'middle_input_{i}')
        
        btn = QPushButton("选择日期")
        btn.clicked.connect(self.openCalendar)
        
        self.cal = QCalendarWidget()
        self.cal.setGridVisible(True)  # 是否显示日期之间的网格
        self.cal.setFixedSize(250, 200)
        self.cal.hide()  # 隐藏日期控件
        self.cal.clicked[QDate].connect(self.showDate)  # clicked[参数]，即定义showDate是传入的参数类型设置
        
        self.middle_layout.addWidget(middle_icon, 2, 0, 1, 1)
        self.middle_layout.addWidget(self.middle_time, 2, 1, 1, self.row - 1)
        self.middle_layout.addWidget(btn, 2, self.row, 1, 1)
        self.middle_layout.addWidget(self.cal, 3, 1, 1, 1)
        
        self.middle_layout.setAlignment(Qt.AlignTop)
        self._obj.mid_layout.addWidget(middle_widget, 0, 0, 1, 1)
        
        set_first_mode_style(middle_widget)
        return True
    
    def showDate(self, date):
        self.middle_time.setText(date.toString("yyyy-MM-dd dddd"))
        self.cal.close()  # 关闭日期控件
    
    def openCalendar(self):
        self.cal.show()  # 显示日期控件
    
    def get_data(self):
        self.children = self.middle_layout.count()
        print(self.children)
        keys = [self.middle_layout.itemAt(i).widget().text() for i in range(self.children) if not (i % 3)]
        values = [self.middle_layout.itemAt(i).widget().text() for i in range(self.children) if i % 3 == 1]
        for i in range(self.children // 3):
            input_val = values[i].strip()
            if not input_val:
                continue
            elif not os.path.exists(input_val):
                print("file path error")
                return
            else:
                self.data[keys[i]] = input_val
        return True
    
    def set_widget_enable(self, flag=False):
        # 禁止btn等
        if flag:
            self.reset_progress()
        else:
            self._obj.tail_btn.setEnabled(True)
        for widget in (self.middle_layout.itemAt(i).widget() for i in range(self.children) if i % 3):
            widget.setDisabled(flag)
    
    def run(self):
        if not self.get_data():
            raise GetDataError("获取页面路径错误")
        if not self.data:
            print("界面参数不能为空")
            return
        try:
            self.create_thread_run()
        except:
            self.set_widget_enable()
            traceback.print_exc()
    
    def create_thread_run(self):
        self._thread = MyThread()
        self._thread.sig_str.connect(self.output_log_info)
        self._thread.sig_int.connect(self.set_progress)
        # self._thread.get_data(self.data)
        self._thread.get_obj(self)
        # 线程启动时禁止button和重置进度条
        # 运行后控件禁止再点击
        self.set_widget_enable(True)
        self._thread.start()


class MyThread(QThread):
    sig_str = pyqtSignal(str)
    sig_int = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)
        self._obj = None
    
    def get_obj(self, obj):
        self._obj = obj
    
    def success(self):
        self.sig_int.emit(const.HUNDRED)
        self.sig_str.emit(f"《{self._obj.name}》_解析完成...")
    
    def set_process(self, value):
        self.sig_int.emit(value)
    
    def log_info(self, value):
        self.sig_str.emit(value)
    
    def run(self):
        print("Thread_result: %s" % self._obj.data)
        try:
            for i in range(1, 100):
                if not (i % 5):
                    self.log_info(f"string_{i}")
                    continue
                sleep(1)
                self.set_process(i)
            self.success()
        except:
            self._obj.set_widget_enable()
            traceback.print_exc()
