# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from cabbage.common.serialize.serialization import Serialization
from zope.interface.declarations import implementer
try:
    import cPickle as pickle
except ImportError:
    import pickle


@implementer(Serialization)
class PickleSerialization():
    TYPE=1002
    def serialize(self,data):
        if data is None:
            return None
        
        return pickle.dumps(data)
        
    def deserialize(self,datas):
        if datas is None:
            return None
        
        return pickle.loads(datas)


    
if __name__=='__main__':
    pass