#!/usr/bin/python3
# -*- coding: utf-8 -*-


# 初始化加载样式
def set_style(obj):
    obj.main_widget.setStyleSheet("""
        #Analysis{
            border:1px solid grey;
            background: white;
            text-align:left;
        }
        #slide_roll_bar{
            border: none;
        }
        QScrollBar::handle:horizontal {
            background: darkGray;
        }
        QScrollBar:horizontal {
            background: #009CAB;
        }

    """)
    obj.up_widget.setStyleSheet("""
        #up_widget{background:#006CAB;}
    """)
    obj.head_widget.setStyleSheet("""
        QToolButton{
            border:none;
        }
        QToolButton:hover{border-bottom:2px solid #F76677;}
    """)
    obj.mid_widget.setStyleSheet("""
            #mid_widget{
                background:white;
                border-top-left-radius: 5px;
                border-bottom-left-radius: 5px;
            }
            #showText{
                border:none;
                background:white;
            }
        """)
    obj.down_widget.setStyleSheet("""
        #execute{
            background:#009CAB;
            font-size:15px;
            font-weight: bold;
            border-radius:2px;
            color: white;
        }
        #execute:hover{
            color:red;
        }
    """)


# notice更新样式
def set_notice_style(widget, args):
    num = len(args) - 1
    notice_btn_css = """#slide_roll_bar{border: none;}QScrollBar::handle:horizontal
                        {background:darkGray;}QScrollBar:horizontal{background: #009CAB;}
                     """
    css_white = "#%s{border:1px solid grey;background:white;text-align:left;}"
    css = "#%s{border:1px solid grey;background:#006CAB;text-align:left;}" * num + css_white + notice_btn_css
    widget.setStyleSheet(css % args)


# 中侧背景色
def set_mid_widget_background_style(widget, flag=True):
    if flag:
        widget.setStyleSheet("""
            #mid_widget{
                background:white;
                border-top-left-radius: 5px;
                border-bottom-left-radius: 5px;
            }
        """)
    else:
        widget.setStyleSheet("""
            #mid_widget{background:#009CAB;}
        """)


# 设置图标是否选中样式
def set_ico_style(widget, name):
    widget.setStyleSheet("""
        QToolButton{border:none;}
        QToolButton:hover{border-bottom:2px solid #F76677;}
        #%s{
            border:1px dashed black;
        }
    """ % name)


# 模块First CSS Style
def set_first_mode_style(widget):
    widget.setStyleSheet("""
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
