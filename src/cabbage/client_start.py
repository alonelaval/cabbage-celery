# -*- encoding: utf-8 -*-
'''
Created on 2016年6月13日

@author: hua
'''
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.scheduler.scheduler_holder import \
    JobManageHolder
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.config import ConfigHolder
from cabbage.constants import READY, ON_LINE, OFF_LINE, REMOVE, \
    BASE, CLIENT_FILE_DIRECTORY, QUEUES, WORKS, CABBAGE, NODE, STATUS, CFG_PATH
from cabbage.data.entity import Work
from cabbage.data.store_factory import storeFactory
from cabbage.event.client_jobs_event import registerClientEvent
from cabbage.process.cabbage_control_holder import \
    CabbageControlHolder
from cabbage.scheduler.cabbage_scheduler import clientScheduler
from cabbage.utils.host_name import HOST_NAME, LOCAL_IP
from cabbage.utils.util import singleton
from cabbage.watch.client_jobs_watch import jobChildWatch, \
    workBrokerQueueWatch, workStatusWatch
from cabbage.watch.server_jobs_watch import configWatch
import os
import sys
import threading
import time
import tornado.ioloop

reload(sys)  
sys.setdefaultencoding('utf8')

def run():
    CabbageControlHolder.getCabbageControl().startCelery()
    
def scheduler():
    clientScheduler()
    JobManageHolder.getJobManage().start()

@singleton
class CabbageClient():
    def __init__(self,cfgPath=None):
        path = ConfigHolder.getConfig().getProperty(BASE,CLIENT_FILE_DIRECTORY)
        self.kazooClient = ZookeeperClientHolder.getRetryClient()
        if not os.path.isdir(path):
            os.makedirs(path)
        
        if not self.kazooClient.isExistPath("/cabbage/jobs"):
            self.kazooClient.create("/cabbage/jobs", makepath=True)
            self.kazooClient.create("/cabbage/jobs/readies", makepath=True)
        if not self.kazooClient.isExistPath("/cabbage/works"):
            self.kazooClient.create("/cabbage/works", makepath=True)
            self.kazooClient.create("/cabbage/works/readies")
        registerClientEvent()
        self.status=OFF_LINE
#         self._initConifg()
        os.environ.setdefault(CABBAGE, NODE)
        
    def _initConifg(self):
        CONFIG_PATH="/cabbage/config"
#         if not self.kazooClient.isExistPath(CONFIG_PATH):
#             self.kazooClient.create(CONFIG_PATH, makepath=True)
#              
#             for key,value in ConfigHolder.getConfig().items(BASE):
#                 self.kazooClient.createPersistent(CONFIG_PATH+"/"+key,value)
                
        self.kazooClient.addChildListener(CONFIG_PATH, configWatch)
        
    def start(self):
        work=Work()
        work.hostName=HOST_NAME
        work.port="1024"
        work.ip = LOCAL_IP
       
        work.status=READY
        
        with storeFactory.store() as store:
            if not store.isExistWork(work):
                store.saveWork(work)
                CacheHolder.getCache().put(HOST_NAME,work,WORKS)
            else:
                CacheHolder.getCache().put(HOST_NAME,store.getWork(HOST_NAME),WORKS)
                store.updateWorkStatus(work)
            
            self.runCeleryServer(work,store)
            
        t2 = threading.Thread(target=scheduler)
        t2.setDaemon(True)
        t2.start()
        tornado.ioloop.IOLoop.current().start()
        
    def runCeleryServer(self,work,store):
        self.kazooClient.addChildListener("/cabbage/jobs/readies", jobChildWatch)
        self.kazooClient.addChildListener("/cabbage/works/"+HOST_NAME+"/"+QUEUES,workBrokerQueueWatch)
        self.kazooClient.addDataListener("/cabbage/works/"+HOST_NAME+"/"+STATUS,workStatusWatch)
        
        #创建临时路径，在节点死的时候，服务端收到信号
        self.kazooClient.create("/cabbage/works/"+HOST_NAME+"/"+ON_LINE,ephemeral=True)
        
        
        self.t1 = threading.Thread(target=run)
        self.t1.setDaemon(True)
        self.t1.start()
        
        def checkStatus(num=1):
            time.sleep(num*5)
            app = CabbageControlHolder.getCabbageControl().cabbage.getApp()
            pingResult = CabbageControlHolder.getCabbageControl().cabbage.ping(work.hostName)
            if app and len(pingResult) >0:
                work.status=ON_LINE
                self.status = ON_LINE
                store.updateWorkStatus(work)
                return
             
            checkStatus(num+1)
             
        self.t2 = threading.Thread(target=checkStatus)
        self.t2.setDaemon(True)
        self.t2.start()
            
            
             
    def offLine(self):
        CabbageControlHolder.getCabbageControl().stopCelery()
        
    def onLine(self):
        work=Work()
        work.hostName=HOST_NAME
        work.status=ON_LINE
        with storeFactory.store() as store:
            self.runCeleryServer(work,store)
            
    
    def stop(self):
        CabbageControlHolder.getCabbageControl().stopCelery()
        work=Work()
        work.hostName=HOST_NAME
        work.status=REMOVE
        self.status = work.status 
        with storeFactory.store() as store:
            store.updateWorkStatus(work)
            
        tornado.ioloop.IOLoop.current().stop()
    
class CabbageClientHolder():
    @classmethod
    def getClient(cls,cfgPath=None):
        return CabbageClient(cfgPath=cfgPath)
        

if __name__=="__main__":
    CabbageClientHolder.getClient().start()
#     
       
        
        
        