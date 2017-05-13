# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from zope.interface.declarations import implementer
from zope.interface.interface import Interface

class Action(Interface):
    def run(self):
        pass
    
@implementer(Action)
class AbstractAction():
    def __init__(self,message):
        self.message = message