# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from cabbage.message.base_message import AbstractMessage
from unittest.case import TestCase
import unittest

class TestAbstractMessage(TestCase):
    def test_default_serialize(self):
        msg = AbstractMessage()
        msg.aaa=111
        ser = msg.getSerialize()
        print ser.serialize(msg)
    
    def test_default_deserialize(self):
        msg = AbstractMessage()
        msg.aaa=111
        print msg.__dict__
        ser = msg.getSerialize()
        s = ser.serialize(msg)
        print type(ser.deserialize(s))
        
if __name__=='__main__':
    unittest.main()