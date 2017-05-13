# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''
from cabbage.common.redis.redis_client import RedisClient
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, REDIS_IP, REDIS_PORT, \
    REDIS_PWD

class RedisClientHolder:
    @classmethod
    def getClient(self,ip=ConfigHolder.getConfig().getProperty(BASE,REDIS_IP),
                  port=ConfigHolder.getConfig().getProperty(BASE,REDIS_PORT),
                  password=ConfigHolder.getConfig().getProperty(BASE,REDIS_PWD)):
        return RedisClient(ip=ip,port=port,password=password)
    
