# -*- encoding: utf-8 -*-
'''
Created on 2016年8月24日

@author: huawei
'''
from cabbage.data.entity import Work
from unittest.case import TestCase
import unittest
class TestBaseEntity(TestCase):
    def test_base_entity(self):
        work = Work(ip=1,port=2,status=3)
        print work.asDict()
        
if __name__=='__main__':
    unittest.main()