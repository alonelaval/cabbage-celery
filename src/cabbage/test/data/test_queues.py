# -*- encoding: utf-8 -*-
'''
Created on 2016年8月31日

@author: huawei
'''
from cabbage.data.entity import BrokerServer, BrokerQueue
from cabbage.data.store_holder import StoreHolder
from unittest.case import TestCase
import unittest.main

class TestQueues(TestCase):
    def test_save(self):
        test1Uri="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
        test2Uri="amqp://cabbage_celery:cabbage_celery@172.16.4.128:5672/cabbage_vhost"
        test1Ip = "172.16.4.134"
        test2Ip = "172.16.4.128"
        queue1Name="cabbage"
        queue2Name="cabbage2"
        self.testUri= test2Uri
        self.testIp =test2Ip
        self.testQueue =queue2Name
        self.save_broker()
        self.save_queue()
        
        self.testUri= test1Uri
        self.testIp =test1Ip
        self.testQueue =queue1Name
        self.save_broker()
        self.save_queue()
        
    def save_broker(self):
        #cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost
        
        brokeServer = BrokerServer(port="5672",ip=self.testIp,serverType="amqp",connectUri=self.testUri,
                              hostName=self.testQueue ,queues=[self.testQueue ])
        store=StoreHolder.getServerStore()
        store.saveBrokerServer(brokeServer)
        
        brokeServer2 =  store.getBrokerServer(self.testQueue )
        self.assertEqual(brokeServer.hostName, brokeServer2.hostName, "asdfa")
        print brokeServer2.connectUri
        
    def save_queue(self):
          
        brokerQueue = BrokerQueue(server=self.testQueue ,queueName=self.testQueue ,exchangeName=self.testQueue ,routingKey=self.testQueue)
        store=StoreHolder.getServerStore()
        store.saveQueue(brokerQueue)
         
        brokerQueue2 = store.getQueue(self.testQueue)
         
        self.assertEqual(brokerQueue.queueName, brokerQueue2.queueName, "121212")
         
        print brokerQueue2.server
#         
        
#     def test_all(self):
#         store=StoreHolder.getServerStore()
#         print [i.asDict() for  i in store.getBrokerServers()]
#         print [i.asDict() for  i in store.getQueues()]
      
    
if __name__=='__main__':
    unittest.main()
    
    
