# -*- encoding: utf-8 -*-
'''
Created on 2016年9月5日

@author: huawei
'''

from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.log.logger import Logger
from cabbage.constants import WORKS, ON_LINE
from cabbage.data.store_factory import storeFactory
# from cabbage.data.store_holder import StoreHolder
from cabbage.process.cabbage_control_holder import \
    CabbageControlHolder
from cabbage.utils.host_name import HOST_NAME
log = Logger.getLogger(__name__)

def workBrokerQueueChangeHandler(event):
#     CacheHolder.getCache().put(QUEUES,event.brokerQueues,WORKS)
    with storeFactory.store() as store:
        work = store.getWork(HOST_NAME)
    CacheHolder.getCache().put(HOST_NAME,work,WORKS)
    if event.isEvent and (work.status == ON_LINE):
        Logger.info(log,"restart")
        CabbageControlHolder.getCabbageControl().restartCelery()
