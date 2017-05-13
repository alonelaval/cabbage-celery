# -*- encoding: utf-8 -*-
'''
Created on 2016年8月29日

@author: huawei
'''

from cabbage.common.Kombu.kombu_amqp_client import KombuClient
import unittest

class TestKombu(unittest.TestCase):
#     def testAddQueue(self):
#         client = KombuClient()
#         client.addQueue("huawei", "huawei", "huawei")
        
#     def test_sendMessage(self):
#         client = KombuClient()
#         client.sendMessage("huawei","huawei", "huawei")
        
#     def test_clearQueue(self):
#         client = KombuClient()
#         client.clearQueue("huawei")
    
    def testUrl(self):
        client = KombuClient(url="amqp://172.16.41.134")._connect()
    def testDeleteQueue(self):
        client = KombuClient()
        client.deleteQueue("huawei","huawei")
     
     
    def testDeleteExchage(self):
        client = KombuClient()
        client.deleteExchage("huawei")

    
         
if __name__=="__main__":
    unittest.main()