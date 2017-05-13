# -*- encoding: utf-8 -*-
'''
Created on 2016年6月3日

@author: hua
'''
from zope.interface.interface import Interface

DISCONNECTED = 0;
CONNECTED = 1;
RECONNECTED = 2;

# class StateListener(Interface):
#     def stateChanged(self,connected):
#         pass
# 
# class ChildListener(Interface):
#     def childChanged(self, path, childrens):
#         pass

class ZookeeperClient(Interface):
    def create(self,path,ephemeral=False,value=b""):
        pass
    def delete(self, path):
        pass
    def getFullPathChildren(self,path,include_data=False,recursion=False):
        pass
    def getChildren(self,path,include_data=False):
        pass
    
    def addChildListener(self,path,childListener):
        pass
    def removeChildListener(self,path,childListener):
        pass
    def addStateListener(self, statelistener):
        pass
    def removeStateListener(self, statelistener):
        pass
    def putData(self,path,data):
        pass
    def removeData(self,path,data):
        pass
    def getData(self,path):
        pass
    def isExistPath(self,path):
        pass
    
    def isConnected(self):
        pass
    def close(self):
        pass
