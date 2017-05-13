# -*- encoding: utf-8 -*-
'''
Created on 2016年5月31日

@author: hua
'''
from zope.interface.interface import Interface

class ITask(Interface):
    def run(self):
        pass