# -*- encoding: utf-8 -*-
'''
Created on 2016年9月9日

@author: huawei
'''
from celery.backends.base import DisabledBackend
from celery.result import AsyncResult
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import TASK_FAILED, TASK_SUCCEEDED, \
    TASK_SENT, TASK_STARTED, WORKER_ONLINE, WORKER_OFFLINE, TASK_RECEIVED, \
    TASK_REVOKED, TASK_RETRIED, OFF_LINE, ON_LINE, BASE, TASK_FAILLOG_PATH, JOB_ID, \
    JOBS
from cabbage.data.store_holder import StoreHolder
from cabbage.event.server_jobs_event import WorkServiceStatusEvent
from cabbage.job.job_results import jobResults
from cabbage.job.task_cache import TaskCacheHolder
from cabbage.monitor.cabbage_counter import CabbageCounterHolder
from cabbage.monitor.monitor_manager import monitorManager
from cabbage.utils.date_util import getNowDateStr
import os
import zope.event
log = Logger.getLogger(__name__)


# store = StoreHolder.getRetryStore()

def _getJobIdAndTaskName(taskId):
#     with storeFactory.store() as store:
#     data =   StoreHolder.getRedisStaticStore().getTaskId(taskId)
#     if data: 
    jobId = taskId.split("@")[1]
    taskName = taskId.split("@")[2]
    return (jobId,taskName)
    
def _getHostName(event):
    return event['hostname'].split("@")[1]

def taskFailed(state,event,app):
    eventOutDic  = event.copy()
    taskName =None
    try:
        taskId = event['uuid']
        task = state.tasks.get(taskId)
#         
#         taskName  = task.name if task and hasattr(task,'name') else None
#         
#         if hasattr(task,'kwargs') and task.kwargs is not None and JOB_ID in task.kwargs:
#             eventOutDic[JOB_ID] = eval(str(task.kwargs))[JOB_ID] 
#          
#         if eventOutDic[JOB_ID] is None:
#             eventOutDic[JOB_ID] = TaskCacheHolder.getJobCache().get(taskName) 
        
#         if taskName is None or eventOutDic[JOB_ID] is None :
        jobId,taskName = _getJobIdAndTaskName(taskId)
        eventOutDic[JOB_ID]=jobId
         
        job = CacheHolder.getCache().get(eventOutDic[JOB_ID],JOBS)
        
        brokerServer= job.brokerServer
        taskPath = ConfigHolder.getConfig().getProperty(BASE, TASK_FAILLOG_PATH)
         
        if not os.path.isdir(taskPath):
            os.makedirs(taskPath)
         
        dateStr = getNowDateStr()
        with open(taskPath+"/"+brokerServer+"_"+dateStr+".log","a+") as writer:
            writer.write(str(eventOutDic)+"\n")
         
#         with storeFactory.store() as store:
#             store.deleteTaskId(task.id)

#         StoreHolder.getRedisStaticStore().deleteTaskId(taskId)
       
        CabbageCounterHolder.getCabbageCounter().updateTaksFail(taskName, _getHostName(event))
         
    except Exception as e:
        Logger.exception(log)
        
#     with storeFactory.store() as store:
#         store.deleteTaskId(task.id)
   
   
    
def taskSucceeded(state,event,app):
    taskId = event['uuid']
    task = state.tasks.get(taskId)
#     taskName  = task.name if task and hasattr(task,'name') else None
    jobId,taskName = _getJobIdAndTaskName(taskId)
    queueTime=0 
    runtime=0  
#     state.
    #FIXME 经常找不到TASK.name
    #@TODO 
    log.debug("【%s】 TASK SUCCEEDED  !"%(event['uuid']))
    try:
#         jobId= None
#         if hasattr(task,'kwargs') and task.kwargs is not None and JOB_ID in task.kwargs:
#             jobId= eval(str(task.kwargs))[JOB_ID]
#              
#         if jobId is None and taskName:
#             jobId = TaskCacheHolder.getJobCache().get(taskName)
#         
#         if taskName is None or jobId is None:
#             jobId,taskName = _getJobIdAndTaskName(taskId)
#             print jobId,taskName
          
        job = CacheHolder.getCache().get(jobId,JOBS)
        
        result = AsyncResult(taskId,app=CabbageHolder.getServerCabbage(job.brokerServer).getApp())
        
        if not isinstance(result.backend, DisabledBackend): 
            log.debug("【%s】 TASK SUCCEEDED result【%s】 !"%(event['uuid'],result.result))
            if result.result:
                jobResults.addResult(jobId, result.result)
                
        
         
# #     print task.started - task.received
#     print queueTime
#         print "task.started:%s"%task.started
#         print "task.received:%s"%task.received
#         print "task.runtime:%s" % event['runtime']
#         print event
        if task and  task.started and task.received:
            queueTime=  task.started - task.received
        runtime=  event['runtime']
        
#         with storeFactory.store() as store:
#             store.deleteTaskId( taskId)
       
        CabbageCounterHolder.getCabbageCounter().updateTaskSucceeded(taskName, _getHostName(event),runtime,queueTime)
#         raise Exception("test")
    except Exception as e:
        Logger.exception(log)
    
#     StoreHolder.getRedisStaticStore().deleteTaskId(taskId)
        
#     with storeFactory.store() as store:
#         store.deleteTaskId(task.id)
    
#     log.info("%s"% task)
#     print task.name
#     print "monitor"
#     print event
#     print dir(task)
#     print task.sent
#     print task.started
#     print task.received
#     print task.succeeded
#     print task.runtime
#     print event['runtime']
#     CabbageCounterHolder.getCabbageCounter().updateTaskSucceeded(taskName, _getHostName(event),runtime,queueTime)
    

def taskSent(state,event,app):
#     task = state.tasks.get(event['uuid'])
#     log.info("%s"% task)
#     print task.name
#     print "monitor"
#     print event
#     print dir(task)
    try:
        taskName= event['name']
        taskId = event['uuid']
        
#         jobId = eval(str(event['kwargs']))[JOB_ID] 
        jobId = TaskCacheHolder.getJobCache().get(taskName)
#         StoreHolder.getRedisStaticStore().saveTaskId(jobId, taskName, taskId)
        
        CabbageCounterHolder.getCabbageCounter().updateTaksSent(taskName)
    except:
        Logger.exception(log)
        
        
def taskReceived(state,event,app):
#     task = state.tasks.get(event['uuid'])
    log.debug("%s"% event)
#     print task.name
#     print "monitor"
#     print event
#     print dir(task)
    try:
        CabbageCounterHolder.getCabbageCounter().updateTaskReceived(event['name'],_getHostName(event))
    except :
        Logger.exception(log)

def workerOnline(state,event,app):
    log.info("【%s】 online !"%_getHostName(event))
    zope.event.notify(WorkServiceStatusEvent(_getHostName(event),ON_LINE))

def workerOffline(state,event,app):
    log.info("【%s】 offline !"% _getHostName(event))
    zope.event.notify(WorkServiceStatusEvent(_getHostName(event),OFF_LINE))
    
def taskStarted(state,event,app):
    pass

def taskRevoked(state,event,app):
    taskId = event['uuid']
#     with storeFactory.store() as store:
#         store.deleteTaskId( taskId)
#     StoreHolder.getRedisStaticStore().deleteTaskId(taskId)

def taskRetried(state,event,app):
    pass


def registerMoniters():
    monitorManager.register(taskSent, TASK_SENT)
    monitorManager.register(taskFailed, TASK_FAILED)
    monitorManager.register(taskSucceeded, TASK_SUCCEEDED)
    monitorManager.register(taskReceived, TASK_RECEIVED)
    monitorManager.register(workerOnline, WORKER_ONLINE)
    monitorManager.register(workerOffline, WORKER_OFFLINE)
    
#     monitorManager.register(taskStarted, TASK_STARTED)
#     monitorManager.register(taskRevoked, TASK_REVOKED)
#     monitorManager.register(taskRetried, TASK_RETRIED)