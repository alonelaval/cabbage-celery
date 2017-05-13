# -*- encoding: utf-8 -*-
'''
Created on 2016年6月17日

@author: hua
'''
# from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.log.logger import Logger
from cabbage.constants import READY, ON_LINE, JOBS, JOB_DELETE
from cabbage.data.store_factory import storeFactory
# from cabbage.data.store_holder import StoreHolder
from cabbage.process.cabbage_control_holder import \
    CabbageControlHolder
from cabbage.utils.host_name import HOST_NAME
log = Logger.getLogger(__name__)
def jobStatusChangeHandler(event):
#     Logger.info(log, "---------jobStatusChangeHandler-----------")
#     try:
#         with storeFactory.store() as store:
#             work = store.getWork(HOST_NAME)
#             job = store.getJob(event.jobId)
            
#         if event and event.jobId and job.status==JOB_DELETE:
    log.info("节点：【%s】删除 job:【%s】"%(HOST_NAME,event.jobId))
#             CabbageControlHolder.getCabbageControl().removeJobId(event.jobId)
    CabbageControlHolder.getCabbageControl().restartCelery()
#     except:
#         Logger.exception(log)
        