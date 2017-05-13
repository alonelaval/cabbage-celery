# -*- encoding: utf-8 -*-
'''
Created on 2016年9月21日

@author: huawei
'''
from unittest.case import TestCase
import unittest
from hdfs.client import Client
class TestHDFS(TestCase):
    def test_request(self):
        client = Client(url="http://10.0.137.24:50070")
        print client.list("/user/cabbage",status=True)
        print client.status("/user/cabbage")
#         pass
            
    def test_respone(self):
        pass
    
if __name__=="__main__":
    unittest.main()
