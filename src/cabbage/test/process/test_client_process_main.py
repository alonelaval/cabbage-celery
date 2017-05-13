# -*- encoding: utf-8 -*-
'''
Created on 2016年6月14日

@author: hua
'''
# from cabbage.common.log import logger
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, CLIENT_FILE_DIRECTORY
from cabbage.data.entity import Work
from cabbage.data.zookeeper_store import ZookeeperStore
from cabbage.event.client_jobs_event import registerClientEvent
from cabbage.event.server_jobs_event import registerServerEvent
from cabbage.process.cabbage_control_holder import \
    CabbageControlHolder
from cabbage.utils.host_name import getHostName
from cabbage.watch.client_jobs_watch import jobChildWatch
import os
import sys
import threading
import time
import unittest
reload(sys)  
sys.setdefaultencoding('utf8')

def run():
    CabbageControlHolder.getCabbageControl().startCelery()
            
class TestClientProcess():
    def run(self):
        registerClientEvent()
        work=Work()
        work.hostName=getHostName()
        work.port="1024"
        work.status="aa"
        
        self.kazooClient = ZookeeperClientHolder.getClient()
        self.store=ZookeeperStore()
        self.kazooClient.addChildListener("/cabbage/jobs", jobChildWatch)
        self.store.saveWork(work)
        
        self.t1 = threading.Thread(target=run)
        self.t1.setDaemon(True)
        self.t1.start()
        time.sleep(5)
        self.app = CabbageHolder.getCabbage().getApp()
        
#         clientDir = ConfigHolder.getConfig().getProperty(BASE,CLIENT_FILE_DIRECTORY)
#         if os.path.exists(clientDir) is False:
#             os.mkdir(clientDir)
       
        
        time.sleep(10)
        
        i = self.app.control.inspect()
        result = i.stats()
        print result
        print i.registered_tasks()
        print self.app.events.State().workers.items()
#         self.t1.join()
        

if __name__=="__main__":
    test = TestClientProcess()
    test.run()