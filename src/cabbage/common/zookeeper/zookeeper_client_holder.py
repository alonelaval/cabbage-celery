# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''
from cabbage.common.zookeeper.kazoo_zookeeper_client import \
    KazooZookeeperClient
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, ZOOKEEPER
from kazoo.retry import KazooRetry

class ZookeeperClientHolder:
    @classmethod
    def getClient(self,connection_retry=None):
        return KazooZookeeperClient(ConfigHolder.getConfig().getProperty(BASE,ZOOKEEPER),connection_retry=connection_retry)
    
    @classmethod
    def getRetryClient(self):
        retry = KazooRetry(max_tries=1000,delay=0.1,backoff=2,max_jitter=0.8,max_delay=3600, ignore_expire=True)
        return KazooZookeeperClient(ConfigHolder.getConfig().getProperty(BASE,ZOOKEEPER),connection_retry=retry)