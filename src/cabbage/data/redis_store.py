# -*- encoding: utf-8 -*-
'''
Created on 2016年11月18日

@author: huawei
'''

from cabbage.common.redis.redis_client_holder import \
    RedisClientHolder
from cabbage.data.store import Store
# from cabbage.utils.util import singleton
from zope.interface.declarations import implementer
@implementer(Store)
class RedisStore(object):
    
    def __init__(self):
        self.redisClient = RedisClientHolder().getClient()
        
    def saveTaskId(self,jobId,taskName,taskId):
        value=str(jobId+"@"+taskName)
        self.redisClient.put(taskId,value)
        
    def getTaskId(self,taskId):
        return self.redisClient.get(taskId)

    def deleteTaskId(self,taskId):
        self.redisClient.delete(taskId)
        