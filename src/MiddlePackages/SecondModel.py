#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import traceback
from time import sleep

import qtawesome
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton

from utils.Style import set_first_mode_style
from MiddlePackages.ABCclass import MiddleWidget, GetDataError


class SecondMode(MiddleWidget):
    def __init__(self, obj, name):
        super().__init__(obj, name)
        self._thread = None
        self._obj = obj
        self.name = name
        self.row = 10
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
        
        self._obj.mid_layout.addWidget(middle_widget, 0, 0, 1, 1)
        
        set_first_mode_style(middle_widget)
        return True
    
    def get_data(self):
        self.children = self.middle_layout.count()
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
            print("界面参数不能为空...")
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
    sig_int = pyqtSignal(int)
    sig_str = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)
        self._obj = None
    
    def get_obj(self, obj):
        self._obj = obj

    def success(self):
        self.sig_int.emit(100)
        self.sig_str.emit(f"《{self._obj.name}》：解析完成。。。")

    def set_process(self, value):
        self.sig_int.emit(value)

    def log_info(self, value):
        self.sig_str.emit(value)
    
    def run(self):
        print("Thread_result: %s" % self._obj.data)
        try:
            for step in range(1, 101):
                sleep(0.1)
                self.set_process(step)
            self.success()
        except:
            self._obj.set_widget_enable()
            traceback.print_exc()
