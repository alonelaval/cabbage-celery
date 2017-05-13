# -*- encoding: utf-8 -*-
'''
Created on 2016年8月1日

@author: hua
'''
from cabbage.constants import OFF_LINE, ON_LINE, REMOVE
from cabbage.data.entity import Work
from cabbage.data.store_holder import StoreHolder
from cabbage.utils.host_name import getHostName
import time
import unittest
class TestRun(unittest.TestCase):    
    
    def test_status(self):
        self.store=StoreHolder.getStore()
        work=Work()
        work.hostName=getHostName()
        work.status=OFF_LINE
        self.store.updateWorkStatus(work)
        time.sleep(10)
        work.status=ON_LINE
        self.store.updateWorkStatus(work)
         
        time.sleep(20)
        work.status=REMOVE
        self.store.updateWorkStatus(work)
        

if __name__=="__main__":
    unittest.main()