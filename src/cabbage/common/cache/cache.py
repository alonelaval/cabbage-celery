# -*- encoding: utf-8 -*-
'''
Created on 2016年6月13日

@author: hua
'''
from zope.interface.interface import Interface

class Cache(Interface):
    def get(self,key,region):
        pass
    def put(self,key,value,region):
        pass
    def hasKey(self,key,region):
        pass