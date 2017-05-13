# -*- encoding: utf-8 -*-
'''
Created on 2016年9月6日

@author: huawei
'''
# -*- encoding: utf-8 -*-
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.constants import BROKER_SERVER, QUEUES
from cabbage.data.entity import BrokerServer, BrokerQueue
from cabbage.data.store_holder import StoreHolder
from cabbage.utils.host_name import getHostName
from unittest.case import TestCase
import time
import unittest.main
'''
Created on 2016年8月31日

@author: huawei
'''

def watch(child):
    print child
    
class TestQueue(TestCase):
    def setUp(self):
        self.kazooClient = ZookeeperClientHolder.getClient()
#         self.kazooClient.addChildListener("/cabbage/works/"+getHostName()+"/"++QUEUES,watch)
        
    def test_update(self):
        print self.kazooClient.getData("/cabbage/works/"+getHostName()+"/"+BROKER_SERVER)
        print self.kazooClient.getData("/cabbage/works/"+getHostName()+"/"+QUEUES)
#         for i in range(9,10):
#            
#             print i
#             self.kazooClient.create("/cabbage/works/"+getHostName()+"/"+QUEUES+"/"+ str(i))
#             time.sleep(10)
          
#         
        
#     def test_all(self):
#         store=StoreHolder.getServerStore()
#         print [i.asDict() for  i in store.getBrokerServers()]
#         print [i.asDict() for  i in store.getQueues()]
      
    
if __name__=='__main__':
    unittest.main()
    
    
