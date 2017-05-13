# -*- encoding: utf-8 -*-
'''
Created on 2016年6月13日

@author: hua
'''
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from cabbage.common.cache.cache import Cache
from cabbage.utils.util import singleton
from zope.interface.declarations import implementer
@singleton
@implementer(Cache)
class BeakerCache(object):
    def __init__(self):
        cache_opts = {
            'cache.type': 'memory',
#             'cache.expire':1000000000
           #  'cache.type': 'file',
            # 'cache.data_dir': '/tmp/cache/data',
             #'cache.lock_dir': '/tmp/cache/lock'
        }
        self.cache = CacheManager(**parse_cache_config_options(cache_opts))

    def get(self,key,region):
        return self.cache.get_cache(region).get(key)
    def put(self,key,value,region):
        self.cache.get_cache(region).put(key,value)
    def remove(self,key,region):
        self.cache.get_cache(region).remove_value(key)
        
    def hasKey(self,key,region):
        return self.cache.get_cache(region).has_key(key)
    def getRegion(self,region):
        return self.cache.get_cache(region)
