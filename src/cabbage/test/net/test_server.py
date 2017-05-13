# -*- encoding: utf-8 -*-
'''
Created on 2016年6月7日

@author: hua
'''
from cabbage.net.server_gevent import GeventServer, \
    GeventStreamServer
from unittest.case import TestCase
import threading
import unittest.main

server = GeventServer()

def startServer():
    server.start()

def stopServer():
    server.stop()

class TestServer(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
#     def test_streamServer(self):
#         geventServer = GeventStreamServer()
#         geventServer.start()
    def test_start(self):
        t1 = threading.Thread(target=startServer)
        t1.start()
#         t2 = threading.Thread(target=stopServer)
#         t2.start()
        
#     def test_stop(self):
#         t1 = threading.Thread(target=stopServer)
#         t1.start()
#     
    

if __name__=="__main__":
    unittest.main()
