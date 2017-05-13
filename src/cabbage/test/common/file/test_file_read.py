# -*- encoding: utf-8 -*-
'''
Created on 2016年6月14日

@author: hua
'''
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, SERVER_FILE_DIRECTORY
from unittest.case import TestCase
import unittest

class TestFileStruct(TestCase):
    def test_request(self):
        dirFile = ConfigHolder.getConfig().getProperty(BASE,SERVER_FILE_DIRECTORY)
        print dirFile
        f = open(dirFile+"/test.py")
        print f.read()
        
    def test_respone(self):
        pass
    
if __name__=="__main__":
    unittest.main()
