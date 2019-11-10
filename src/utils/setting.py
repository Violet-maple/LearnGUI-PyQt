#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging
from logging import handlers

import yaml

from utils import const

const.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filename = os.path.join(const.BASE_DIR, 'utils/mode.yaml')


def load_info():
    with open(filename, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_log_config(model_name):
    logging.basicConfig(level=logging.DEBUG,
                        filename=os.path.join(const.BASE_DIR, f'Log/Model-{model_name}.log'),
                        filemode='a',
                        format='%(asctime)s - [line:%(lineno)d]: %(message)s'
                        )


class Logger(object):
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }
    
    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                 fmt2='%(levelname)s: %(message)s',
                 ):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        format_console = logging.Formatter(fmt2)
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_console)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


if __name__ == '__main__':
    res = load_info()
    print([i for i in res])
