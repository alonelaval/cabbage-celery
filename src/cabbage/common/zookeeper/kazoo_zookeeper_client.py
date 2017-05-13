# -*- encoding: utf-8 -*-
'''
Created on 2016年6月3日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.common.zookeeper.zookeeper_client import \
    ZookeeperClient
from cabbage.utils.util import singleton
from kazoo.client import KazooClient, KazooState
# from kazoo.handlers.eventlet import SequentialEventletHandler
# from kazoo.handlers.gevent import SequentialGeventHandler
from zope.interface.declarations import implementer
import six
# from cabbage.utils.util import singleton
# from kazoo.recipe.watchers import ChildrenWatch
log = Logger.getLogger(__name__)
def my_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
        log.info("KazooState.LOST")
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
        log.info("KazooState.SUSPENDED")
    else:
        # Handle being connected/reconnected to Zookeeper
        log.info("KazooState.connected/reconnected")

@implementer(ZookeeperClient)
class KazooZookeeperClient():
    def __init__(self,hosts,connection_retry=None,command_retry=None):
        self.zkclient =KazooClient(hosts=hosts,connection_retry=connection_retry,command_retry=command_retry,timeout=1000)
        self.zkclient.start()
        self.zkclient.add_listener(my_listener)
        

    def create(self,path,ephemeral=False,value=b"",makepath=False):
        if ephemeral:
            self.createEphemeral(path,value=value,makepath=makepath)
        else:
            self.createPersistent(path,value=value,makepath=makepath)
            
    def createEphemeral(self,path,value=b"",makepath=False):
        self.zkclient.create(path,ephemeral=True,value=value,makepath=makepath)
        
    def createPersistent(self,path,value=b"",makepath=False):
        self.zkclient.create(path,value=value,makepath=makepath)
    
    def delete(self, path,recursive=False):
        self.zkclient.delete(path,recursive=recursive)
    
    def getChildren(self,path,include_data=False):
        return  self.zkclient.get_children(path,include_data=include_data)
        
    def getFullPathChildren(self,path,include_data=True,recursion=False):
        childs =[]
        if include_data:
            childs = self.setChildrenPath(path,self.zkclient.get_children(path,include_data=include_data)[0])
        else:
            childs = self.setChildrenPath(path,self.zkclient.get_children(path,include_data=include_data))
        if recursion:
            for child in childs:
                if  isinstance(child, six.string_types):
                    data = (self.getFullPathChildren(child,include_data=include_data,recursion=recursion))
                    childs =  childs +  data
        return  childs;
    
    def setChildrenPath(self,path,childs):
        c = []
        for child in childs:
            c.append(path+"/"+child)
        return c
        
    def addChildListener(self,path,childListener):
#         ChildrenWatch(self.zkclient,path,childListener)
        @self.zkclient.ChildrenWatch(path)
        def f(child):
            return childListener(child)
            
    def removeChildListener(self,path,childListener):
        raise Exception("不支持的操作")
    
    def addDataListener(self,path,childListener):
        @self.zkclient.DataWatch(path)
        def f(data, stat, event=None):
            return childListener(data, stat, event)
        
    def removeDataListener(self,path,childListener):
        raise Exception("不支持的操作")
    
    def addStateListener(self, statelistener):
        self.zkclient.add_listener(statelistener)
    def removeStateListener(self, statelistener):
        self.zkclient.remove_listener(statelistener)
        
    def putData(self,path,data):
        self.zkclient.set(path, data)
        
    def removeData(self,path):
        self.zkclient.set(path, b"")
    
    def getData(self,path):
        return  self.zkclient.get(path)[0]
    def isExistPath(self,path):
        return False if self.zkclient.exists(path) is None else True 
    
    def isConnected(self):
        return self.zkclient.connected
    def state(self):
#         return self.zkclient.start
        pass
    def close(self):
        if self.zkclient.connected:
            self.zkclient.stop()
        
    