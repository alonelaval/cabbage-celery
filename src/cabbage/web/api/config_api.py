# -*- encoding: utf-8 -*-
'''
Created on 2016年9月27日

@author: huawei
'''
from cabbage.common.log.logger import Logger
from cabbage.web.api.util import excute

log = Logger.getLogger(__name__)
class ConfigApi(object):
    @excute
    def getConfigs(self,store):
        return store.getConfigs()
    
