# -*- encoding: utf-8 -*-
'''
Created on 2016年6月13日

@author: hua
'''

from cabbage.common.cache.beaker_cache import BeakerCache
import unittest

class TestBeaker(unittest.TestCase):
    def setUp(self):
        self.cache = BeakerCache()
#     def test_put(self):
#         self.cache.put("jobid", "dd", "job")
#     def test_get(self):
#         self.cache.put("jobid", "dd", "job")
#         print self.cache.get("jobid", "job")
#         
#     def test_haskey(self):
#         self.cache.put("jobid", "dd", "job")
#         print self.cache.hasKey("jobid","job")
#         print self.cache.hasKey("asdfadsf", "asdfasdf")
        
    def test_region(self):
        self.cache.put("jobid", "dd", "job")
        self.cache.put("jobi111d", "dd", "job")
        print dir( self.cache.getRegion("job"))
        print self.cache.getRegion("job").namespace.keys()
    
if __name__=="__main__":
    unittest.main()
