# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''
from cabbage.cabbage_celery import celeryconfig
from cabbage.cabbage_celery.cabbage_for_celery import Cabbage
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, CONNECT_URI, WORKS
from cabbage.data.store_holder import StoreHolder
from cabbage.utils.host_name import HOST_NAME
from kombu.entity import Queue, Exchange


class CabbageHolder:
    servers={}
#     serversDegist
    @classmethod
    def getCabbage(self):
        connectUri = CabbageHolder._getConnectUri()
        work = CacheHolder.getCache().get(HOST_NAME, WORKS)
        if work.queues and len(work.queues)>0:
            queues = []
            for queueName in work.queues:
                brokerQueue = StoreHolder.getStore().getQueue(queueName)
                queues.append(Queue(name=brokerQueue.queueName, exchange=Exchange(brokerQueue.exchangeName), routing_key=brokerQueue.routingKey))
            celeryconfig.CELERY_QUEUES=tuple(queues)
            
        return Cabbage(broker=str(connectUri))
    
    @classmethod
    def _getConnectUri(self):
        connectUri = ConfigHolder.getConfig().getProperty(BASE,CONNECT_URI)
        work = CacheHolder.getCache().get(HOST_NAME, WORKS)
        if work.brokerServer:
            brokerServer = StoreHolder.getStore().getBrokerServer(work.brokerServer)
            connectUri = brokerServer.connectUri
        return connectUri
        
#     @classmethod
#     def getServerCabbage(self):
#         ip = ConfigHolder.getConfig().getProperty(BASE,CONNECT_URI)
#         return Cabbage(broker=str(ip))
    
    @classmethod
    def getServerCabbages(self):
        return CabbageHolder.servers
    
    
    
    @classmethod
    def getServerCabbagesStr(self):
        return CabbageHolder.servers.__str__()
    
    @classmethod
    def getServerCabbage(self,broker):
        return CabbageHolder.servers[broker]
    
    def getRunServerCabbage(self,broker):
        return CabbageHolder.servers[broker]
        
    @classmethod
    def putServerCabbage(self,broker,cabbage):
        CabbageHolder.servers[broker]=cabbage
        
    
    