# -*- encoding: utf-8 -*-
'''
Created on 2016年9月21日

@author: huawei
'''
from unittest.case import TestCase
import unittest


class TestHDFS(TestCase):
    def test_request(self):
        from snakebite.client import Client
        client = Client("10.0.137.24", 8022, use_trash=False)
        for x in client.ls(['/user']):
            print x
            
    def test_respone(self):
        pass
    
if __name__=="__main__":
    unittest.main()
