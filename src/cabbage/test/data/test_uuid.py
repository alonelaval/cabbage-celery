# -*- encoding: utf-8 -*-
'''
Created on 2016年6月8日

@author: hua
'''
from unittest.case import TestCase
import unittest
import uuid

class TestAbstractMessage(TestCase):
    def test_uuid(self):
        print "job-%s"%uuid.uuid4()
if __name__=='__main__':
    unittest.main()