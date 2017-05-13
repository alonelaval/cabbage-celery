# -*- encoding: utf-8 -*-
'''
Created on 2016年8月31日

@author: huawei
'''
from cabbage.common.Kombu.kombu_amqp_client import KombuClient
from cabbage.common.log.logger import Logger
from cabbage.data.entity import BrokerServer
from cabbage.event.server_jobs_event import AddBrokerServerEvent
from cabbage.web.api.util import excute
import zope.event

log = Logger.getLogger(__name__)
class BrokerServerApi(object):
    @excute
    def getBrokerServers(self,store):
        return  store.getBrokerServers()
    @excute
    def addServer(self,store,hostName  , ip , port ,connectUri, serverType):
        try:
            import socket
            socket.create_connection((ip, int(port)),timeout=3)
            KombuClient(url=connectUri)._connect()
        except Exception:
            log.exception(log)
            raise Exception("地址链接不通")
        
        if  store.isExistBrokerServer(hostName):
            raise Exception("名称已经存在！")
        borkerServer = BrokerServer(port=port,ip=ip,serverType=serverType,connectUri=connectUri,hostName=hostName)
        store.saveBrokerServer(borkerServer)
        
        zope.event.notify(AddBrokerServerEvent(borkerServer))
    
    @excute    
    def getBrokerServerByHostname(self,store,hostname):
        return  store.getBrokerServer(hostname)
    
    def remove(self,hostName):
        pass
#          StoreHolder.getServerStore()