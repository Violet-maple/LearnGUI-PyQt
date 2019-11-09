#!/usr/bin/python3
# -*- coding: utf-8 -*-


import qtawesome
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit

from Config.Style import set_first_mode_style
from MiddlePackages.ABCclass import MiddleWidget, GetDataError


class Analysis(MiddleWidget):
    def __init__(self, obj, name):
        super().__init__(obj, name)
        self.middle_text = None
        self._thread = None
        self._name = name
        self._obj = obj
        self.set_up()
    
    def set_up(self):
        self.middle_text = QTextEdit()
        self.middle_text.setText("这是一个textEdit,记录日志")
        # self.middle_text.setDisabled(True)
        self.middle_text.setObjectName('showText')
        self._obj.mid_layout.addWidget(self.middle_text)
        return True
    
    def set_value(self, value):
        self.middle_text.append(value)

    def get_value(self):
        return self.middle_text.toPlainText()
    
    def get_data(self):
        pass
    
    def set_widget_enable(self, flag=False):
        pass
    
    def run(self):
        pass
