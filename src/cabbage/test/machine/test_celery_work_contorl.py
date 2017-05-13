# -*- encoding: utf-8 -*-
'''
Created on 2016年8月1日

@author: hua
'''
from cabbage.constants import OFF_LINE, ON_LINE, REMOVE
from cabbage.data.entity import Work
from cabbage.data.store_holder import StoreHolder
from cabbage.machine.celery_work_contorl import CeleryWorkContorl
from cabbage.server_start import CabbageServerHolder
from cabbage.utils.host_name import getHostName
import time
import unittest
class TestRun(unittest.TestCase):    
    
    def test_status(self):
        work=Work()
        work.hostName=getHostName()
        workContorl = CeleryWorkContorl(work)
        workContorl.stopService()
        time.sleep(10)
        workContorl.startService()
        print workContorl.serviceIsAlive()
        time.sleep(20)
        workContorl.stop()
        
        
        
if __name__=="__main__":
    CabbageServerHolder.getServer().start()
    unittest.main()