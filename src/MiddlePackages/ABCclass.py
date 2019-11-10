#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time

from abc import ABCMeta, abstractmethod

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog

from utils import const


class GetDataError(Exception):
    pass


class MiddleWidget(metaclass=ABCMeta):
    """(抽象类)"""
    row = 5
    height = const.BTN_HEIGHT
    
    def __init__(self, obj, name):
        self.middle_layout = None
        self.data = {}
        self.children = 0
        self.name = name
        self._obj = obj
    
    @pyqtSlot()
    def open_file(self, widget):
        """
        选择文件
        :param widget:
        :result 设置文件路径(写入到上一个输入框)
        :error
        """
        response = QFileDialog.getOpenFileName()
        if isinstance(response, tuple):
            file_path = response[0]
            if not os.path.exists(file_path):
                return
            widget.sender().previousInFocusChain().setText(file_path)
    
    def set_progress(self, value):
        """
        进度条
        :param value: 进度数
        :return: None
        """
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError as e:
                print(e)
                return
        self._obj.progressBar.setValue(value)
        if value >= const.HUNDRED:
            self._obj.tail_btn.setEnabled(True)
            self.set_widget_enable()
    
    def output_log_info(self, msg):
        # old_value = self._obj.container["Analysis"]["modelObj"].get_value()
        # self._obj.container["Analysis"]["modelObj"].set_value(f"{step}\n{old_value}")
        msg = f"{time.strftime('%F %T')} {msg}"
        self._obj.container["Analysis"]["modelObj"].set_value(msg)
    
    def reset_progress(self):
        self._obj.progressBar.reset()
        self._obj.tail_btn.setDisabled(True)
    
    @abstractmethod
    def set_widget_enable(self):
        pass
    
    @abstractmethod
    def get_data(self):
        pass
    
    @abstractmethod
    def run(self):
        pass
