# -*- encoding: utf-8 -*-
'''
Created on 2016年6月8日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, SERVER_FILE_DIRECTORY, MASTER, CABBAGE, \
    ADMIN_NAME, ADMIN_PWD
from cabbage.data.entity import User
from cabbage.data.store_holder import StoreHolder
from cabbage.event.server_jobs_event import registerServerEvent
from cabbage.utils.util import singleton
from cabbage.watch.web_server_watch import configWatch, workWatch, jobWebWatch, \
    brokerServerWatch
from cabbage.web.cabbage_application import CabbageApplicationContorl
import os
import sys
import tornado.ioloop
log = Logger.getLogger(__name__)

reload(sys)  
sys.setdefaultencoding('utf8')

@singleton    
class CabbageWebServer():
    def __init__(self,cfgPath=None):
        self.kazooClient = ZookeeperClientHolder.getClient()
        self.store=StoreHolder.getServerStore()
        registerServerEvent()
        path = ConfigHolder.getConfig().getProperty(BASE,SERVER_FILE_DIRECTORY)
        if not os.path.isdir(path):
            os.makedirs(path)
        self._initConifg()
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
            
        if not self.kazooClient.isExistPath("/cabbage/monitor"):
            self.kazooClient.create("/cabbage/monitor", makepath=True)
            self.kazooClient.create("/cabbage/monitor/jobs")
            self.kazooClient.create("/cabbage/monitor/works")
            self.kazooClient.create("/cabbage/monitor/brokerServers")
            
        if not self.kazooClient.isExistPath("/cabbage/users"):
            self.kazooClient.create("/cabbage/users", makepath=True)
            if not self.kazooClient.isExistPath("/cabbage/users/"+ConfigHolder.getConfig().getProperty(BASE,ADMIN_NAME)):
                self.store.saveUser(User(userName=ConfigHolder.getConfig().getProperty(BASE,ADMIN_NAME),
                                         userPwd=ConfigHolder.getConfig().getProperty(BASE,ADMIN_PWD),isAdmin=True))
            
            
        if not self.kazooClient.isExistPath("/cabbage/queueServer"):
            self.kazooClient.create("/cabbage/queueServer/brokerServers", makepath=True)
            self.kazooClient.create("/cabbage/queueServer/brokerServers/readies")
            self.kazooClient.create("/cabbage/queueServer/queues", makepath=True)
        
        os.environ.setdefault(CABBAGE,MASTER)
            
    def start(self):
        #start web
        CabbageApplicationContorl().start() 
        #fork 子进程接管下面的代码
        from cabbage.data.store_factory import StoreFactory
        client = ZookeeperClientHolder.getClient()
        client.addChildListener("/cabbage/queueServer/brokerServers/readies", brokerServerWatch)
        client.addChildListener("/cabbage/jobs/readies", jobWebWatch)
        client.addChildListener("/cabbage/works/readies", workWatch)
        client.addChildListener("/cabbage/config", configWatch)
        log.info("系统初始化完成！")
      
        tornado.ioloop.IOLoop.current().start()
        
    def stop(self):
        tornado.ioloop.IOLoop.current().stop()
        
class CabbageWebServerHolder():
    @classmethod
    def getServer(cls):
        return CabbageWebServer()
        
# if __name__=="__main__":
#     CabbageServerHolder.getServer().start()
#         
    
    