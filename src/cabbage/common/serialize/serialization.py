# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: huawei
'''
from zope.interface.interface import Interface

class Serialization(Interface):
    def serialize(self,datas):
        pass
    def deserialize(self,datas):
        pass