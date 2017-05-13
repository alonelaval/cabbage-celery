# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: huawei
'''
from cabbage.utils.bytes import int2bytes, bytes2int, int2hex, \
    int2BytesPack, bytes2IntUnpack
from unittest.case import TestCase
import unittest

class TestBytes(TestCase):
    

#     def test_int_to_byte(self):
#         i = 1024
#         print int2hex(i)
#         print len(int2bytes(i))
#         
#     def test_byte_to_int(self):
#         i = 1024
#         bs = int2bytes(i)
#         print "test_byte_to_int"
#         print bytes2int(bs)
    
    def test_byte_to_int_pack(self):
        i = 1024
        print len(int2BytesPack(i))
    
    def test_int_to_byte_unpack(self):
        i = 1024
        bs = int2BytesPack(i)
        print "test_int_to_byte_unpack"
        print bytes2IntUnpack(bs)

if __name__=="__main__":
    unittest.main()
