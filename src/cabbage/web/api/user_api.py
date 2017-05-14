# -*- encoding: utf-8 -*-
'''
Created on 2017年5月14日

@author: huawei
'''
from cabbage.common.log.logger import Logger
from cabbage.web.api.util import excute

log = Logger.getLogger(__name__)

class UserApi(object):
    @excute
    def getUser(self,store,userName):
        return store.getUser(userName)
    
