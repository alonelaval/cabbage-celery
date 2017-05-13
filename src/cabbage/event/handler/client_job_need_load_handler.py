# -*- encoding: utf-8 -*-
'''
Created on 2016年6月17日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.constants import READY, ON_LINE
from cabbage.data.store_factory import storeFactory
# from cabbage.data.store_holder import StoreHolder
from cabbage.process.cabbage_control_holder import \
    CabbageControlHolder
from cabbage.utils.host_name import HOST_NAME
log = Logger.getLogger(__name__)
def jobNeedLoadHandler(event):
    with storeFactory.store() as store:
        work = store.getWork(HOST_NAME)
    if event and event.jobId :
#         CabbageControlHolder.getCabbageControl().addJobId(event.jobId)
        CabbageControlHolder.getCabbageControl().restartCelery()
