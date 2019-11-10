#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import traceback

import qtawesome
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtWidgets import (QWidget, QMainWindow, QGridLayout,
                             QPushButton, QToolButton, QApplication,
                             QDesktopWidget, QScrollBar, QProgressBar, QLabel)

from utils import const
from utils.Style import set_mid_widget_background_style, set_ico_style, set_notice_style, set_style
from MiddlePackages.AnalysisModle import Analysis
from MiddlePackages.BMain import ObjFactory
from utils.setting import load_info
from main import QTitleButton, QTitleLabel


class MainUi(QMainWindow):
    obj_num = 0
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
        self.slide.setFixedHeight(const.SLIDE_HEIGHT)
        self.slide.setMaximum(self.column)
        self.slide.setMinimum(self.num)
        self.slide.valueChanged.connect(self._value_change)
        
        # 创建日志记录
        name = "Analysis"
        self.notice_btn = QPushButton(name)
        self.notice_btn.setObjectName(name)
        self.container["selectedNoticeName"] = name
        self.notice_btn.setFixedSize(const.NOTICE_WIDTH, const.BTN_HEIGHT)
        self.notice_btn.clicked.connect(self._clicked)
        
        # 创建中侧部件
        self.mid_widget = QWidget()
        self.mid_widget.setObjectName('mid_widget')
        # self.mid_widget.setFixedHeight(400)
        self.mid_layout = QGridLayout()
        self.mid_widget.setLayout(self.mid_layout)
        
        # 创建下侧部件
        self.down_widget = QWidget()
        self.down_widget.setObjectName('down_widget')
        self.down_widget.setFixedHeight(60)
        self.down_layout = QGridLayout()
        self.down_widget.setLayout(self.down_layout)
        
        self.main_layout.addWidget(self.up_widget, 0, 0, 1, self.column)
        self.main_layout.addWidget(self.slide, 1, 0, 1, self.column)
        self.main_layout.addWidget(self.notice_btn, 2, 0, 1, 1)
        self.main_layout.addWidget(self.mid_widget, 3, 1, 1, self.column - 1)
        self.main_layout.addWidget(self.down_widget, 4, self.column - 1, 1, 1)
        self.setCentralWidget(self.main_widget)
        
        # 生成analysis
        analysis = Analysis(self, name)
        self.container[name] = {"noticeName": name, "modelObj": analysis, "index": self.obj_num}
        self.container["selectedModelName"] = name
        
        # 创建头部（head）
        self.head_widget = QWidget()
        self.head_layout = QGridLayout()
        self.head_widget.setLayout(self.head_layout)
        
        self.load_model_ico(0, self.num) if self.num < self.column else self.load_model_ico(0, self.column)
        self.up_layout.addWidget(self.head_widget, 0, 0, 0, 0)
        # 创建中部
        
        # 创建尾部 按钮
        self.tail_btn = QPushButton("Execute")
        self.tail_btn.setObjectName('execute')
        self.tail_btn.setFixedSize(const.TAIL_HEIGHT, const.BTN_HEIGHT)
        self.tail_btn.clicked.connect(self.run)
        
        self.down_layout.addWidget(self.tail_btn, 0, 0, 0, 0)
        self.down_layout.setAlignment(Qt.AlignRight)
        # 展示进度条
        self.progressBar = QProgressBar()
        label = QLabel()
        label.setText("运行进度：")
        
        self.statusBar().addPermanentWidget(label)
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setAlignment(Qt.AlignLeft)
        self.progressBar.setMaximum(const.HUNDRED)
        self.progressBar.setValue(const.ZERO)
        
        self.main_layout.setSpacing(const.ZERO)
        
        set_style(self)
        # self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
    
    def run(self):
        mode_name = self.container.get("selectedModelName", "")
        mode_info = self.container.get(mode_name, {})
        mode = mode_info.get("modelObj")
        if not mode:
            print("error %s" % mode)
            return
        try:
            mode.run()
        except:
            self.set_progress()
            traceback.print_exc()
    
    def set_progress(self):
        self.tail_btn.setEnabled(True)
    
    # def flush(self):
    #     while self.progressBar.text() != "100%":
    #         QApplication.processEvents()
    #         sleep(0.1)
    #     self.tail_btn.setEnabled(True)
    #     print("flush over")
    
    def load_model_ico(self, start, end):
        for i in range(start, end):
            self.tool_btn = QToolButton()
            self.tool_btn.setText(f"{self.icon[i]}")  # 设置按钮文本
            self.tool_btn.setObjectName(f"{self.icon[i]}")  # 设置按钮文本
            self.tool_btn.setFixedSize(85, 52)
            self.tool_btn.setIcon(qtawesome.icon(f'fa.{self.icon[i]}', color='white'))  # 设置按钮图标
            self.tool_btn.setIconSize(QSize(const.ICO_SIZE, const.ICO_SIZE))  # 设置图标大小
            self.tool_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            self.tool_btn.clicked.connect(self._clicked)
            
            self.head_layout.addWidget(self.tool_btn, 0, i, 1, 1)
    
    def info_btn(self, name):
        notice_btn = QPushButton(name)
        notice_btn.setObjectName(f"{name}_{self.obj_num}")
        notice_btn.setFixedSize(const.NOTICE_WIDTH, const.BTN_HEIGHT)
        self.container[name]["noticeName"] = f"{name}_{self.obj_num}"
        notice_btn.clicked.connect(self._clicked)
        
        self.main_layout.addWidget(notice_btn, 2, self.obj_num, 1, 1)
    
    def _clicked(self):
        model_name = self.sender().text()
        if model_name == self.container.get("selectedModelName"):
            self.show_widget(model_name)
            return  # message.info()
        self.statusBar().showMessage(f'Current Value is {model_name}')
        model_info = self.container.get(model_name, {})
        if not model_info:
            mode = None
            try:
                mode = ObjFactory.create(self, model_name)
            except:
                traceback.print_exc()
                # return  # message.info()
            if mode is None:
                set_mid_widget_background_style(self.mid_widget, False)
                self.show_widget(model_name)
                print("failed")
                return  # message.info()
            model_info["modelObj"] = mode
            self.obj_num += 1
            model_info["index"] = self.obj_num
            self.container[model_name] = model_info
            self.info_btn(model_name)
        self.show_widget(model_name)
        self.show()
    
    @staticmethod
    def del_layout(layout):
        for i in range(layout.count()):
            layout.itemAt(i).widget().deleteLater()
    
    def show_widget(self, curr_mode_name):
        previous_name = self.container.get("selectedModelName")
        if previous_name is not None:
            index = self.container.get(previous_name).get("index")
            if index is not None:
                self.mid_layout.itemAt(index).widget().close()
        index = self.container.get(curr_mode_name, {}).get("index")
        if index is None:
            set_ico_style(self.head_widget, curr_mode_name)
            self.show_notice_widget(curr_mode_name)
            return
        self.mid_layout.itemAt(index).widget().show()
        self.show_notice_widget(curr_mode_name)
        set_mid_widget_background_style(self.mid_widget)
        set_ico_style(self.head_widget, curr_mode_name)
        self.container["selectedModelName"] = curr_mode_name
        print(f"当前Container：{self.container}")
        print(f"当前选中模块：{curr_mode_name}")
    
    def show_notice_widget(self, model_name):
        curr_notice_name = self.container.get(model_name, {}).get("noticeName", "failed-model")
        args = []
        for key, item in self.container.items():
            if not isinstance(item, dict):
                continue
            elif key == model_name:
                continue
            else:
                args.append(item.get("noticeName"))
        args.append(curr_notice_name)
        set_notice_style(self.main_widget, tuple(args))
        
        self.container["selectedNoticeName"] = curr_notice_name
    
    def _value_change(self):
        value = self.slide.value()
        start = value - self.num
        self.statusBar().showMessage(f'Current Value is {value}')
        self.del_layout(self.head_layout)
        self.load_model_ico(start, value)
    
    def paintEvent(self, event):
        # 设置背景颜色
        painter = QPainter(self)
        background_color = QColor()
        background_color.setNamedColor('#006CAB')
        painter.setBrush(background_color)
        painter.drawRect(self.rect())
    
    def _center(self):
        # 窗口居中
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
    
    # #**************************************************** ##
    # #**************************************************** ##
    # #**************************************************** ##
    # #**************************************************** ##
    def setCloseButton(self, bool):
        # 给widget定义一个setCloseButton函数，为True时设置一个关闭按钮
        if bool == True:
            self._CloseButton = QTitleButton(b'\xef\x81\xb2'.decode("utf-8"), self)
            self._CloseButton.setObjectName("CloseButton")  # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._CloseButton.setToolTip("关闭窗口")
            self._CloseButton.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._CloseButton.setFixedSize(20, 20)  # 设置按钮高度为标题栏高度
            self._CloseButton.clicked.connect(self.close)  # 按钮信号连接到关闭窗口的槽函数
            self.up_layout.addWidget(self._CloseButton, 0, self.column, 0, 0)
            self.up_layout.setAlignment(Qt.AlignAbsolute)
    
    def setMinMaxButtons(self, bool):
        # 给widget定义一个setMinMaxButtons函数，为True时设置一组最小化最大化按钮
        if bool == True:
            self._MinimumButton = QTitleButton(b'\xef\x80\xb0'.decode("utf-8"), self)
            self._MinimumButton.setObjectName("MinMaxButton")  # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._MinimumButton.setToolTip("最小化")
            self._MinimumButton.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._MinimumButton.setFixedHeight(2)  # 设置按钮高度为标题栏高度
            self._MinimumButton.clicked.connect(self.showMinimized)  # 按钮信号连接到最小化窗口的槽函数
            self._MaximumButton = QTitleButton(b'\xef\x80\xb1'.decode("utf-8"), self)
            self._MaximumButton.setObjectName("MinMaxButton")  # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._MaximumButton.setToolTip("最大化")
            self._MaximumButton.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._MaximumButton.setFixedHeight(2)  # 设置按钮高度为标题栏高度
            self._MaximumButton.clicked.connect(self._changeNormalButton)  # 按钮信号连接切换到恢复窗口大小按钮函数
    
    def _changeNormalButton(self):
        # 切换到恢复窗口大小按钮
        try:
            self.showMaximized()  # 先实现窗口最大化
            self._MaximumButton.setText(b'\xef\x80\xb2'.decode("utf-8"))  # 更改按钮文本
            self._MaximumButton.setToolTip("恢复")  # 更改按钮提示
            self._MaximumButton.disconnect()  # 断开原本的信号槽连接
            self._MaximumButton.clicked.connect(self._changeMaxButton)  # 重新连接信号和槽
        except:
            pass
    
    def _changeMaxButton(self):
        # 切换到最大化按钮
        try:
            self.showNormal()
            self._MaximumButton.setText(b'\xef\x80\xb1'.decode("utf-8"))
            self._MaximumButton.setToolTip("最大化")
            self._MaximumButton.disconnect()
            self._MaximumButton.clicked.connect(self._changeNormalButton)
        except:
            pass
    
    def initTitleLabel(self):
        # 安放标题栏标签
        self._TitleLabel = QTitleLabel(self)
        self._TitleLabel.setMouseTracking(True)  # 设置标题栏标签鼠标跟踪（如不设，则标题栏内在widget上层，无法实现跟踪）
        self._TitleLabel.setIndent(2)  # 设置标题栏文本缩进
        # self._TitleLabel.move(580, 580)  # 标题栏安放到左上角
        self.main_layout.addWidget(self._TitleLabel, 0, self.column, 1, 1)


def main():
    app = QApplication(sys.argv)
    gui = MainUi(load_info())
    # gui.setCloseButton(True)
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
