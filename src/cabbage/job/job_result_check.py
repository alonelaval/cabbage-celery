# -*- encoding: utf-8 -*-
'''
Created on 2016年9月22日

@author: huawei
'''

from celery.result import AsyncResult
from celery.states import SUCCESS, FAILURE
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import JOBS, BASE, TASK_FAILLOG_PATH, \
    ON_LINE
from cabbage.data.store_holder import StoreHolder
from cabbage.job.job_cache import JobCacheHolder
from cabbage.job.job_results import jobResults
from cabbage.monitor.cabbage_counter import CabbageCounterHolder

from cabbage.utils.date_util import getNowDateStr
import os
log = Logger.getLogger(__name__)
# class JobResultCheck(object):
#     def __init__(self):
#         pass
#     
#     def run(self):
#         for jobId,jobProcess in JobCacheHolder.getJobCache().items():
#             for result in jobProcess.results:
#                 if result.state == SUCCESS:
#                         if result.result and result.result != "":
#                             jobResults.addResult(jobId,result.result)
#                         jobProcess.results.remove(result)
#                 if result.state == FAILURE:
#                     jobProcess.results.remove(result)

def checkResult():
    jobIds =  StoreHolder.getServerStore().getRunJobs()
    for jobId in  jobIds:
        job = CacheHolder.getCache().get(jobId,JOBS)
        tasks = StoreHolder.getServerStore().getTaskIdsByJobId(jobId)
        
        for taskName,taskIds in tasks.items():
            for taskId in taskIds:
#                 state = CabbageHolder.getServerCabbage(job.brokerServer).getApp().events.State()
                job = CacheHolder.getCache().get(jobId,JOBS)
                result = AsyncResult(taskId,app=CabbageHolder.getServerCabbage(job.brokerServer).getApp())
#                 print  result._get_task_meta()
                if result.state == SUCCESS:
                    data = result.result
                    if data and data != "":
                        jobResults.addResult(jobId,data)
    #                 queueTime=  task.started - task.received
                    CabbageCounterHolder.getCabbageCounter().updateTaskSucceeded(taskName,"unknown", 0,0)
                    
                    StoreHolder.getServerStore().deleteTaskId(jobId,taskName, taskId)
                    
                if result.state == FAILURE:
                    data = {}
                    data['traceback']=result.traceback()
                    data['uuid']=taskId
                    data['jobId']=jobId
                    
                    taskPath = ConfigHolder.getConfig().getProperty(BASE, TASK_FAILLOG_PATH)
                     
                    if not os.path.isdir(taskPath):
                        os.makedirs(taskPath)
                     
                    dateStr = getNowDateStr()
                    with open(taskPath+"/"+job.brokerServer+"_"+dateStr+".log","a+") as writer:
                        writer.write(str(data))
                    
                    CabbageCounterHolder.getCabbageCounter().updateTaksFail(taskName,"unknown")
                    
                    StoreHolder.getServerStore().deleteTaskId(jobId, taskName,taskId)
                    
    from cabbage.server_start import CabbageServerHolder
    CabbageServerHolder.getServer().status = ON_LINE
#             
                
                
                