#!/usr/bin/python3
# -*- coding: utf-8 -*-

from MiddlePackages.FirstModle import FirstMode
from MiddlePackages.SecondModel import SecondMode
from MiddlePackages.thirdModel import ThirdMode


class ObjFactory:
    """创建工厂（工厂模式 - 通过工厂实现对象使用者和对象之间的解耦合）"""
    
    @staticmethod
    def create(obj, model_name):
        """创建对象"""
        mode = None
        if model_name == 'forward':
            mode = FirstMode(obj, model_name)
        elif model_name == 'sellsy':
            mode = SecondMode(obj, model_name)
        elif model_name == 'film':
            mode = ThirdMode(obj, model_name)
        return mode
