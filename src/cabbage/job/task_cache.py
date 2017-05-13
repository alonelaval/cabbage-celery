# -*- encoding: utf-8 -*-
'''
Created on 2016年9月12日

@author: huawei
'''

class TaskCache():
    def __init__(self):
        self.store={}
    def get(self,key):
        if key in self.store:
            return self.store.get(key)
    def put(self,key,value):
        self.store[key]=value
    def keys(self):
        return self.store.keys()
    def values(self):
        return self.store.values()
    def items(self):
        return self.store.items()
    def remove(self,key):
        del self.store[key]
    def has_key(self,key):
        return self.store.has_key(key)
    
taskCache = TaskCache()

class TaskCacheHolder():
    @classmethod
    def getJobCache(self):
        return taskCache