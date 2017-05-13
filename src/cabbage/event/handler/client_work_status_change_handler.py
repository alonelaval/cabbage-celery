# -*- encoding: utf-8 -*-
'''
Created on 2016年10月9日

@author: huawei
'''

from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.constants import WORKS, READY, ON_LINE, OFF_LINE, \
    REMOVE
from cabbage.data.store_factory import storeFactory
# from cabbage.data.store_holder import StoreHolder
from cabbage.process.cabbage_control_holder import \
    CabbageControlHolder
from cabbage.utils.host_name import HOST_NAME
import threading
    

    
def clentWorkStatusChangeHandler(event):
    from cabbage.client_start import CabbageClientHolder
    hostName=HOST_NAME
#     work = StoreHolder.getStore().getWork(hostName)
    with storeFactory.store() as store:
        work = store.getWork(hostName)
    CacheHolder.getCache().put(hostName,work,WORKS)
    
    clentStatus= CabbageClientHolder.getClient().status
    
    if event.status == OFF_LINE and clentStatus == ON_LINE:
        CabbageControlHolder.getCabbageControl().stopCelery(hostName)
        CabbageClientHolder.getClient().status=OFF_LINE
        
    if event.status == ON_LINE  and  clentStatus == OFF_LINE : 
#         def run():
        CabbageClientHolder.getClient().status=ON_LINE
        CabbageControlHolder.getCabbageControl().restartCelery()
#         t1 = threading.Thread(target=run)
#         t1.setDaemon(True)
#         t1.start()
        
    if event.status == REMOVE and clentStatus != REMOVE:
        CabbageClientHolder.getClient().stop()
        
