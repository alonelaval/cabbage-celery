# -*- encoding: utf-8 -*-
'''
Created on 2016年11月18日

@author: huawei
'''
from redis import Redis
from redis.connection import ConnectionPool
class RedisClient():
    
    def __init__(self,ip="",port=6379,defalutDb=1,max_connections=30,password=""):
        self.pool = ConnectionPool(host=ip, port=port, db=defalutDb,max_connections=max_connections,password=password)
        self.redis = Redis(connection_pool=self.pool)
        
    def get(self,key):
        return self.redis.get(key)
    
    def put(self,key,value,ex=60 * 60 * 24 * 5):
        '''
            ex:默认过期时间为5天，如果一个task 5天都没有跑完，直接丢弃记录
            
        '''
        self.redis.set(key, value,ex=ex)
    
    def delete(self,key):
        self.redis.delete(key)
        
    def isConnected(self):
        return self.redis.ping()
    