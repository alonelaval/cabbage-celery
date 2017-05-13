# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: huawei
'''
from cabbage.utils.bytes import bytes2IntUnpack, int2BytesPack
from zope.interface.declarations import implementer
from zope.interface.interface import Interface

MAGIC = 1024 #草榴社区
HEAD_LEN=16
MAGIC=1024

class Codec(Interface):
    '''
        head = 16字节
        MAGIC = 1024  4byte
        messageId  =   4byte
        serialize  =   4byte
        messageLength = 4byte
        iii
    '''
    def decode(self,datas):
        pass
    def encode(self,message):
        pass

@implementer(Codec)
class  MessageCodec():
    def __init__(self):
        pass
    
    def decode(self,datas):
        magic= bytes2IntUnpack(datas[0:4])[0]
        if magic == MAGIC:
            self.messageId=bytes2IntUnpack(datas[4:8])[0]
            self.serialize=bytes2IntUnpack(datas[8:12])[0]
            self.messageLength=bytes2IntUnpack(datas[12:16])[0]
        else:
            raise  Exception("magic cannot match!")
     
    def encode(self,message):
        datas = message.getData()
        serialize = message.getSerialize().TYPE
        magic = int2BytesPack(MAGIC)
        messageId = int2BytesPack(message.messageId)
        serialize = int2BytesPack(serialize)
        messageLength = int2BytesPack(len(datas))
        return magic+messageId+serialize+messageLength+datas
    
        
        