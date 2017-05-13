# -*- encoding: utf-8 -*-
'''
Created on 2016年6月3日

@author: hua
'''
from cabbage.file.file_struct import FileResponseStruct, \
    FileRequestStruct
from unittest.case import TestCase
import struct
import unittest

class TestFileStruct(TestCase):
    def test_request(self):
        filePath="test"
        print struct.pack("ii4s",1024,4,filePath)
        
        f = FileRequestStruct(filePath)
        bytedatas = f.encode()
        print bytedatas
        f.decode(bytedatas)
        
        self.assertEqual(filePath, f.filePath)
        
    
    def test_respone(self):
        pass
    
if __name__=="__main__":
    unittest.main()
