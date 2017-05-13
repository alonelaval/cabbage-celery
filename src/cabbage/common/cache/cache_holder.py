# -*- encoding: utf-8 -*-
'''
Created on 2016年6月13日

@author: hua
'''
from cabbage.common.cache.beaker_cache import BeakerCache

# beakcache = BeakerCache()

class CacheHolder():
    @classmethod
    def getCache(self):
        return BeakerCache()