# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from cabbage.common.serialize.json_serialization import \
    JosnSerialization
from zope.interface.declarations import implementer
from zope.interface.interface import Interface

class Message(Interface):
    def doAction(self):
        pass
    def getData(self):
        pass
    def getSerialize(self):
        pass

@implementer(Message)
class AbstractMessage():
    def doAction(self):
        return self.getAction().run()

    def getData(self):
        return self.getSerialize().serialize(self)
    
    def getSerialize(self):
        return JosnSerialization(self)
    
    def getAction(self):
        pass 


    