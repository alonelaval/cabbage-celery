# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from cabbage.common.serialize.serialization import Serialization
from zope.interface.declarations import implementer
import json


@implementer(Serialization)
class JosnSerialization():
    TYPE=1001
    def __init__(self,objType=None):
        self.objType=objType
        
    def serialize(self,data):
        if data is None:
            return None
        if self.objType:
            return json.dumps(data, default=lambda objType: self.objType.__dict__)
        return json.dumps(data)
        
    def deserialize(self,datas):
        if datas is None:
            return None
        if self.objType:
            return json.loads(datas)
        return json.loads(datas)

if __name__=='__main__':
    pass