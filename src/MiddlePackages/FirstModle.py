#!/usr/bin/python3
# -*- coding: utf-8 -*-

import qtawesome
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog

from MiddlePackages.ABCclass import MiddleWidget


class FirstMode(MiddleWidget):
    def __init__(self, obj, name):
        super().__init__(obj, name)
        self._name = name
        self._obj = obj
        # self.row = 10
    
    def run(self):
        middle_widget = QWidget()
        middle_layout = QGridLayout()
        middle_widget.setLayout(middle_layout)
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
            middle_btn.clicked.connect(lambda: self.select_file(middle_widget))
            
            middle_layout.addWidget(middle_icon, i, 0, 1, 1)
            middle_layout.addWidget(middle_input, i, 1, 1, self.row - 1)
            middle_layout.addWidget(middle_btn, i, self.row, 1, 1)
        
        self._obj.mid_layout.addWidget(middle_widget, 0, 0, 1, 1)
        
        middle_widget.setStyleSheet("""
            QLineEdit{
                padding:5px 2px;
            }
            QPushButton{
                padding:5px 2px;
            }
            QPushButton:hover{
                color:red;font-weight: bold;
            }
        """)
        return True
