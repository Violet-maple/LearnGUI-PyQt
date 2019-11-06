#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from abc import ABCMeta, abstractmethod

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog


class MiddleWidget(metaclass=ABCMeta):
    """(抽象类)"""
    row = 5
    height = 25
    
    def __init__(self, obj, name):
        self._obj = obj
        self._name = name
    
    @pyqtSlot()
    def select_file(self, middle_widget):
        print(10)
        response = QFileDialog.getOpenFileName()
        if isinstance(response, tuple):
            file_path = response[0]
            if not os.path.exists(file_path):
                return
            middle_widget.sender().previousInFocusChain().setText(file_path)
    
    @abstractmethod
    def run(self):
        """运行抽象方法"""
        pass
