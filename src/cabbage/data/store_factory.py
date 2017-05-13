# -*- encoding: utf-8 -*-
'''
Created on 2016年10月31日

@author: huawei
'''
from cabbage.common.pool.connection_pool import \
    ConnectionObjectPool
from cabbage.data.store_holder import StoreHolder
from contextlib import contextmanager


class StoreFactory(object):
    
    def _create(self):
        return StoreHolder.getRetryStore()
    
    def __init__(self,max_size=None):
        self.pool = ConnectionObjectPool(self._create,max_size=max_size)
    
    def getStore(self, timeout=None):
        return self.pool.get( timeout=timeout)
    def returnStroe(self,store):
        self.pool.put(store)
    
    @contextmanager
    def store(self):
        store = self.getStore()
        try:
            yield store
        finally:
            self.returnStroe(store)
    
storeFactory = StoreFactory(max_size=15)
