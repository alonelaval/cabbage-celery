# -*- encoding: utf-8 -*-
'''
Created on 2016年6月24日

@author: hua
'''
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.utils.host_name import getHostName
import unittest

class TestCabbage(unittest.TestCase):
        
    def test_start(self):
        cabbage = CabbageHolder.getCabbage()
        cabbage.start()
#         cabbage.stop("celery@"+getHostName())
#     def test_stop(self):
#         cabbage = CabbageHolder.getCabbage(self)
#         cabbage.stop("")
#         
#     def test_haskey(self):
#         self.cache.put("jobid", "dd", "job")
#         print self.cache.hasKey("jobid","job")
#         print self.cache.hasKey("asdfadsf", "asdfasdf")
        
#     def test_region(self):
#         print self.cache.getRegion("job")
    
if __name__=="__main__":
    unittest.main()
