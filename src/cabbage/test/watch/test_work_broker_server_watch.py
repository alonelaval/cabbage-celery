# -*- encoding: utf-8 -*-
'''
Created on 2016年9月6日

@author: huawei
'''
# -*- encoding: utf-8 -*-
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.constants import BROKER_SERVER
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

def watch(data,stat,event):
    print data,stat,event

class TestServer(TestCase):
    def setUp(self):
        self.kazooClient = ZookeeperClientHolder.getClient()
#         self.kazooClient.addDataListener("/cabbage/works/"+getHostName()+"/"+BROKER_SERVER,watch)
    def test_update(self):
        for i in range(5):
            print i
            self.kazooClient.putData("/cabbage/works/"+getHostName()+"/"+BROKER_SERVER, str(i))
            time.sleep(10)
#         
        
#     def test_all(self):
#         store=StoreHolder.getServerStore()
#         print [i.asDict() for  i in store.getBrokerServers()]
#         print [i.asDict() for  i in store.getQueues()]
      
    
if __name__=='__main__':
    unittest.main()
    
    
