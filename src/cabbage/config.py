# -*- encoding: utf-8 -*-
'''
Created on 2016年6月14日

@author: hua
'''
from collections import defaultdict
from cabbage.constants import CFG_PATH
from cabbage.utils.util import singleton
import ConfigParser
import os


@singleton
class Config(object):
    
    def __init__(self,cfgPath=None):
        self.cfg = ConfigParser.ConfigParser()
#         CONFIG_PATH="/cabbage/config"
        self.changeListeners=defaultdict(set)
        if cfgPath:
            self.cfg.read(cfgPath)
        else:
            self.cfg.read(os.getcwd().split("cabbage")[0]+'/cabbage/cabbage.cfg')
            
    def __call__(self):
        from cabbage.common.zookeeper.zookeeper_client_holder import ZookeeperClientHolder
        kazooClient = ZookeeperClientHolder.getClient()
        CONFIG_PATH="/cabbage/config"
        from cabbage.watch.server_jobs_watch import configWatch
        kazooClient.addChildListener(CONFIG_PATH, configWatch)
        
    def addChangeListerner(self,key,changeListerner):
        self.changeListeners[key].add(changeListerner)
        
    def getProperty(self,region, key):
        return self.cfg.get(region, key)
    def items(self,region):
        return self.cfg.items(region)
    
    def hasProperty(self,region,key):
        return self.cfg.has_option(region, key)
    
    def setProperty(self,region,key,value):
        self.cfg.set(region, key, value)
        self.onChange(key, value)
        
    def onChange(self,key,value):
        for listener in self.changeListeners[key]:
            listener(key,value)

class ConfigHolder(object):
    @classmethod
    def getConfig(self,cfgPath=None):
        if cfgPath is None:
            cfgPath = os.environ.get(CFG_PATH)
            if cfgPath =="":
                cfgPath =None
        return Config(cfgPath=cfgPath)
    
    
# ConfigHolder.getConfig()()