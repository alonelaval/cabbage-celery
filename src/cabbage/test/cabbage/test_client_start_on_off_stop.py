# -*- encoding: utf-8 -*-
'''
Created on 2016年8月1日

@author: hua
'''
from cabbage.client_start import CabbageClient
from tornado import ioloop
import unittest
class TestRun(unittest.TestCase):    
    
    def test_run(self):
        
        client = CabbageClient()
        client.start()
        print "-----start-----"
        client.offLine()
        print "------offLine-----"
        client.onLine()
        print "------onLine-------"
        client.stop()
        print "------stop----------"
#         ioloop.IOLoop.current().start()

if __name__=="__main__":
    unittest.main()