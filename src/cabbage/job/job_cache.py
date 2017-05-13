# -*- encoding: utf-8 -*-
'''
Created on 2016年8月23日

@author: hua
'''
# from cabbage.utils.util import singleton
# @singleton
class JobCache():
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
    def has_key(self,key):
        return self.store.has_key(key)

jobCache = JobCache()

class JobCacheHolder():
    @classmethod
    def getJobCache(self):
        return jobCache