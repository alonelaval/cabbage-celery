# -*- encoding: utf-8 -*-
'''
Created on 2016年6月13日

@author: hua
'''
# from cabbage.common.zookeeper.zookeeper_client_holder import \
#     ZookeeperClientHolder
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, REDIS_PORT, REDIS_IP
from cabbage.data.redis_store import RedisStore
from cabbage.data.server_zookeeper_store import \
    ServerZookeeperStore
from cabbage.data.zookeeper_store import ZookeeperStore
# from kazoo.retry import KazooRetry
store = ZookeeperStore()
redisStore = RedisStore()

class StoreHolder:
    @classmethod
    def getStore(self):
        return  ZookeeperStore()
    @classmethod
    def getStaticStore(self):
        return store
    
    @classmethod
    def getRetryStore(self):
#         retry = KazooRetry(max_tries=1000,delay=0.1,backoff=2,max_jitter=0.8,max_delay=3600, ignore_expire=True)
#         client= ZookeeperClientHolder.getClient(connection_retry=retry)
        return ZookeeperStore(isRetry=True)
    
    @classmethod
    def getRedisStaticStore(self): 
        return redisStore
    
    @classmethod
    def getServerStore(self):
        return ServerZookeeperStore()