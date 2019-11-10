#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys


class _Const(object):
    class ConstError(TypeError):
        pass
    
    class ConstCaseError(ConstError):
        pass
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't Change Const.%s" % name)
        if not name.isupper():
            raise self.ConstCaseError('Const Name "%s" is not all Super Case' % name)
        
        self.__dict__[name] = value
    
    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError("Can't Unbind Const(%s)" % name)
        raise NameError(name)


constant = _Const()
sys.modules[__name__] = constant
# 增加常量
# constant.PI = 3.14
constant.SLIDE_HEIGHT = 8
constant.NOTICE_WIDTH = 150
constant.BTN_HEIGHT = 25
constant.TAIL_HEIGHT = 80
constant.HUNDRED = 100
constant.ZERO = 0
constant.ICO_SIZE = 35
