# -*- encoding: utf-8 -*-
'''
Created on 2016年6月8日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.common.scheduler.scheduler_holder import \
    JobManageHolder
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, SERVER_FILE_DIRECTORY, MASTER, \
    CABBAGE
from cabbage.data.store_holder import StoreHolder
from cabbage.event.server_jobs_event import \
    registerServerEvent #     AddBrokerServerEvent, MonitorBrokerServerEvent
from cabbage.net.server_gevent import GeventStreamServer
from cabbage.queue.job_queue import JobEventPoolHolder
from cabbage.utils.util import singleton
from cabbage.watch.monitor_server_watch import jobReadyWatch, \
    configWatch, workWatch, brokerServerWatch
from cabbage.web.cabbage_application import \
    CabbageApplicationContorl
import os
import sys
import threading
import time
import tornado.ioloop
import zope.event
log = Logger.getLogger(__name__)

reload(sys)  
sys.setdefaultencoding('utf8')

def start_file_server():
    geventServer = GeventStreamServer()
    geventServer.start()
     
def start_jobPool(): 
    JobEventPoolHolder.getJobEventPool().start()
def start_web():
    CabbageApplicationContorl().start()
    tornado.ioloop.IOLoop.current().start()
def scheduler():
    JobManageHolder.getJobManage().start()
    
    
@singleton    
class CabbageServer():
    def __init__(self,cfgPath=None):
        self.kazooClient = ZookeeperClientHolder.getRetryClient()
        self.store=StoreHolder.getServerStore()
        registerServerEvent()
        path = ConfigHolder.getConfig().getProperty(BASE,SERVER_FILE_DIRECTORY)
        if not os.path.isdir(path):
            os.makedirs(path)
#         self._initConifg()
        self._initData()
        self.status=None
        
    def _initConifg(self):
        CONFIG_PATH="/cabbage/config"
        if not self.kazooClient.isExistPath(CONFIG_PATH):
            self.kazooClient.create(CONFIG_PATH, makepath=True)
            
            for key,value in ConfigHolder.getConfig().items(BASE):
                self.kazooClient.createPersistent(CONFIG_PATH+"/"+key,value)
            
        self.kazooClient.addChildListener(CONFIG_PATH, configWatch)
        
        
    def _initData(self):
        if not self.kazooClient.isExistPath("/cabbage/jobs"):
            self.kazooClient.create("/cabbage/jobs", makepath=True)
            self.kazooClient.create("/cabbage/jobs/readies", makepath=True)
            self.kazooClient.create("/cabbage/jobs/results")
        if not self.kazooClient.isExistPath("/cabbage/works"):
            self.kazooClient.create("/cabbage/works", makepath=True)
            self.kazooClient.create("/cabbage/works/readies")
#         else:
#             works = self.store.getWorks()
#             for work in works:
#                 work.status =REMOVE
#                 self.store.updateWorkStatus(work)
        
        if not self.kazooClient.isExistPath("/cabbage/monitor"):
            self.kazooClient.create("/cabbage/monitor", makepath=True)
            self.kazooClient.create("/cabbage/monitor/jobs")
            self.kazooClient.create("/cabbage/monitor/works")
            self.kazooClient.create("/cabbage/monitor/brokerServers")
            
            
        if not self.kazooClient.isExistPath("/cabbage/queueServer"):
            self.kazooClient.create("/cabbage/queueServer/brokerServers", makepath=True)
            self.kazooClient.create("/cabbage/queueServer/brokerServers/readies")
            self.kazooClient.create("/cabbage/queueServer/queues", makepath=True)
#         else:
#             brokers = self.store.getBrokerServers()
#             for borker in brokers:
#                 zope.event.notify(AddBrokerServerEvent(borker))
#                 zope.event.notify(MonitorBrokerServerEvent(borker))
            
        self.kazooClient.addChildListener("/cabbage/queueServer/brokerServers/readies", brokerServerWatch)
        self.kazooClient.addChildListener("/cabbage/works/readies", workWatch)
        os.environ.setdefault(CABBAGE,MASTER)
            
    def start(self):
        #start web
#         CabbageApplicationContorl().start()
        self.kazooClient.addChildListener("/cabbage/jobs/readies", jobReadyWatch)
#         process = multiprocessing.Process(target=start_web)
#         process.start()
        #start fileServer
        t1 = threading.Thread(target=start_file_server)
        t1.setDaemon(True)
        t1.start()
#         process = multiprocessing.Process(target=start_server)
#         process.start()
        
        
        from cabbage.scheduler.cabbage_scheduler import serverScheduler
        serverScheduler()
        t2 = threading.Thread(target=scheduler)
        t2.setDaemon(True)
        t2.start()
        time.sleep(5)
#         checkResult()
        log.info("系统初始化完成！")
        tornado.ioloop.IOLoop.current().start()
        
        
    def stop(self):
#         geventServer = GeventStreamServer()
#         geventServer.stop()
        tornado.ioloop.IOLoop.current().stop()
        
class CabbageServerHolder():
    @classmethod
    def getServer(cls):
        return CabbageServer()
        
# if __name__=="__main__":
#     CabbageServerHolder.getServer().start()
#         
    
    