# -*- encoding: utf-8 -*-
'''
Created on 2016年6月14日

@author: hua
'''
# from cabbage.common.log import logger
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.constants import JOB_AUTH_PASS
from cabbage.data.store_holder import StoreHolder
from cabbage.data.zookeeper_store import ZookeeperStore
from cabbage.event.client_jobs_event import registerClientEvent
from cabbage.event.server_jobs_event import registerServerEvent, \
    JobRunEvent
from cabbage.net.server_gevent import GeventStreamServer
from cabbage.process.cabbage_control_holder import \
    CabbageControlHolder
from cabbage.watch.client_jobs_watch import jobChildWatch
import threading
import time
import unittest
import zope.event

def run():
    CabbageControlHolder.getCabbageControl().startCelery()

def start_server():
    geventServer = GeventStreamServer()
    geventServer.start()
    
class TestClientProcess(unittest.TestCase):
    def setUp(self):
        registerClientEvent()
        registerServerEvent()
        self.t1 = threading.Thread(target=run)
        self.t1.setDaemon(True)
        self.t1.start()
        time.sleep(5)
        
        time.sleep(5)
        self.t2 = threading.Thread(target=start_server)
        self.t2.setDaemon(True)
        self.t2.start()
        self.app = CabbageHolder.getCabbage().getApp()
        
    def test_client_process(self):
            
        self.kazooClient = ZookeeperClientHolder.getClient()
        self.store=ZookeeperStore()
        self.kazooClient.addChildListener("/cabbage/jobs", jobChildWatch)
        
        time.sleep(10)
        self.jobId="123456789"
        print dir(self.store.getJob(self.jobId))
        self.store.updateAuditStatus(self.jobId,JOB_AUTH_PASS)
        time.sleep(10)
        for i in range(10):
            zope.event.notify(JobRunEvent("123456789"))
        
        i = self.app.control.inspect()
        result = i.stats()
        print result
        print i.registered_tasks()
        self.t2.join()
        self.t1.join()
        

if __name__=="__main__":
    unittest.main()