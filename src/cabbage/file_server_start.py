# -*- encoding: utf-8 -*-
'''
Created on 2016年6月8日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, SERVER_FILE_DIRECTORY
from cabbage.data.store_holder import StoreHolder
from cabbage.net.server_gevent import GeventStreamServer
from cabbage.utils.util import singleton
from cabbage.watch.server_jobs_watch import configWatch
import os
import sys
import zope.event
log = Logger.getLogger(__name__)

reload(sys)  
sys.setdefaultencoding('utf8')

def start_server():
    geventServer = GeventStreamServer()
    geventServer.start()
    
    
@singleton
class CabbageFileServer():
    def __init__(self,cfgPath=None):
        path = ConfigHolder.getConfig(cfgPath=cfgPath).getProperty(BASE,SERVER_FILE_DIRECTORY)
        if not os.path.isdir(path):
            os.makedirs(path)
        self.kazooClient = ZookeeperClientHolder.getRetryClient()
        self.store=StoreHolder.getServerStore()
        self.status=None
        self._initConifg()
        
    def _initConifg(self):
        CONFIG_PATH="/cabbage/config"
        if not self.kazooClient.isExistPath(CONFIG_PATH):
            self.kazooClient.create(CONFIG_PATH, makepath=True)
            
            for key,value in ConfigHolder.getConfig().items(BASE):
                self.kazooClient.createPersistent(CONFIG_PATH+"/"+key,value)
            
        self.kazooClient.addChildListener(CONFIG_PATH, configWatch)
    def start(self):
        geventServer = GeventStreamServer()
        geventServer.start()
        
        
    def stop(self):
        geventServer = GeventStreamServer()
        geventServer.stop()
        
class CabbageFileServerHolder():
    @classmethod
    def getServer(cls,cfgPath=None):
        return CabbageFileServer(cfgPath=cfgPath)
        
    
    