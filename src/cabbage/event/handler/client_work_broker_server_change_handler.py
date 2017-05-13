# -*- encoding: utf-8 -*-
'''
Created on 2016年9月5日

@author: huawei
'''

from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.constants import WORKS, QUEUES, READY, ON_LINE
from cabbage.data.store_factory import storeFactory
from cabbage.data.store_holder import StoreHolder
from cabbage.process.cabbage_control_holder import \
    CabbageControlHolder
from cabbage.utils.host_name import HOST_NAME


def workBrokerServerChangeHandler(event):
    print "------workBrokerServerChangeHandler-----------"
    hostName=HOST_NAME
#     work = StoreHolder.getStore().getWork(hostName)
    with storeFactory.store() as store:
        work = store.getWork(hostName)
#     CacheHolder.getCache().put(QUEUES,work.queues,WORKS)
    CacheHolder.getCache().put(hostName,work,WORKS)
    
    if event.isEvent and (work.status == READY or work.status == ON_LINE):
#         parent="/"+CABBAGE+"/"+WORKS+"/"+hostName
#         from cabbage.watch.client_jobs_watch import workBrokerServerWatch
#         ZookeeperClientHolder.getClient().addDataListener(parent+"/"+BROKER_SERVER, workBrokerServerWatch)
        CabbageControlHolder.getCabbageControl().restartCelery()
