# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''
from unittest.case import TestCase
import time
import unittest


class TestTimeStamp(TestCase):
    def test_time_stamp(self):
        timeStamp = 1381419600
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print otherStyleTime
        d = str(time.time())
        print time.localtime(float(d))
        
if __name__=='__main__':
    unittest.main()