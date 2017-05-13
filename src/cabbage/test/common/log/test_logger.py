# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: huawei
'''
from cabbage.common.log import logger
from unittest.case import TestCase
import logging
import os
import sys
import unittest

class TestLogger(TestCase):
    
    def test_conf_path(self):
        print os.getcwd().split("cabbage")[0]+'cabbage/logging.conf'
#         print os.lisdir('/')

    def test_logger(self):
        logger.Logger.getLogger("simpleExample").debug("test")
        
    def test_loggin_debug(self):
        logging.debug("test")

if __name__=="__main__":
    unittest.main()
