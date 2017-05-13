# -*- encoding: utf-8 -*-
'''
Created on 2016年6月7日

@author: hua
'''
from cabbage.message.file_message import FileRequestMessage
from cabbage.net.client import SocketClient
from unittest.case import TestCase
import traceback
import unittest.main

class TestClient(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
#     def test_start(self):
#         client = SocketClient()
#         client.connect()
#         requestMessage = FileRequestMessage()
#         requestMessage.filePath ="12121212"
#         requestMessage.fileName ="asdfasdfasdf"
#         client.sendall(requestMessage)
    def test_server(self):
        try:
            client = SocketClient()
            client.connect()
            requestMessage = FileRequestMessage()
            requestMessage.filePath ="12121212"
            requestMessage.fileName ="asdfasdfasdf"
            client.sendall(requestMessage)
        except Exception:
            traceback.print_exc()

if __name__=="__main__":
    unittest.main()