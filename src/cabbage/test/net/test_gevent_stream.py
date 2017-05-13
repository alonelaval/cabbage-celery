# -*- encoding: utf-8 -*-
'''
Created on 2016年6月7日

@author: hua
'''
from cabbage.net.server_gevent import GeventServer, \
    GeventStreamServer
from unittest.case import TestCase
import unittest.main

server = GeventServer()

class TestServer(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
    def test_streamServer(self):
        geventServer = GeventStreamServer()
        geventServer.start()
#     
    

if __name__=="__main__":
    unittest.main()
