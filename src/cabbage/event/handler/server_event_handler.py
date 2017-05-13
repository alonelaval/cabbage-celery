# -*- encoding: utf-8 -*-
'''
Created on 2016年7月11日

@author: hua
'''
from cabbage.cabbage_celery.cabbage_for_celery import Cabbage
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.log.logger import Logger
from cabbage.constants import JOBS, JOB_DELETE, WORKS
from cabbage.data.store_factory import storeFactory
from cabbage.job.job_cache import JobCacheHolder
from cabbage.job.job_holder import JobHolder
from cabbage.job.task_cache import TaskCacheHolder
from cabbage.monitor.celery_monitor import cabbage_monitor
import threading
log = Logger.getLogger(__name__)


def workServiceStatusHandler(event):
    if event:
        work = CacheHolder.getCache().get(event.hostName,WORKS)
        if work:
            work.serviceStatus=event.status
            with storeFactory.store() as store:
                store.updateWorkServiceStatus(work)
                
def workStatusHandler(event):
    if event:
        work = CacheHolder.getCache().get(event.hostName,WORKS)
        if work:
            work.status=event.status
            with storeFactory.store() as store:
                store.updateWorkStatus(work)
            
def addBroberServerHandler(event):
    if event and event.brokerServer:
        brokerServer = event.brokerServer
        Logger.info(log,"添加队列服务器【%s】,URI:【%s】"%( brokerServer.hostName,brokerServer.connectUri))
        cabbage = Cabbage(hostName=brokerServer.hostName,broker=brokerServer.connectUri)
        
        CabbageHolder.getServerCabbages()[brokerServer.hostName]= cabbage
        Logger.debug(log,"添加队列服务器【%s】"% CabbageHolder.getServerCabbagesStr())
        
def monitorBroberServerHandler(event):
    if event and event.brokerServer:
        brokerServer = event.brokerServer
        cabbage = CabbageHolder.getServerCabbages().get(brokerServer.hostName)
        def monitor(cabbage):
            Logger.info(log, "添加监控【%s】,URI:【%s】"%( brokerServer.hostName,brokerServer.connectUri))
            cabbage_monitor(cabbage.getApp())
            Logger.info(log, "添加监控结束")
        t1 = threading.Thread(target=monitor,args=(cabbage,))
        t1.setDaemon(True)
        t1.start()
    
def jobUpdateHandler(event):
    jobId = event.jobId
    status = event.status
    if status == JOB_DELETE:
        jobRun = JobCacheHolder.getJobCache().get(jobId)
        if jobRun : #停止运行TASK
            jobRun.stop()
        with storeFactory.store() as store:
            store.updateJobStatus(jobId, JOB_DELETE)
        #删除缓存让下一个task可以同名
        tasks=CacheHolder.getCache().get(jobId, JOBS).tasks
        for taskName in tasks:
            if TaskCacheHolder.getJobCache().has_key(taskName):
                TaskCacheHolder.getJobCache().remove(taskName)
            
    with storeFactory.store() as store:
        job=store.getJob(jobId)
        CacheHolder.getCache().put(jobId, job,JOBS)

def jobRemoveHandler(event):
    try:
        jobId = event.jobId
        if  JobCacheHolder.getJobCache().has_key(jobId):
            jobRun = JobCacheHolder.getJobCache().get(jobId)
            if jobRun : #停止运行TASK
                jobRun.stop()
            else:
                job =CacheHolder.getCache().get(jobId, JOBS)
                for taskName in job.tasks:
                    CabbageHolder.getServerCabbage(job.brokerServer).revokeByTaskName(taskName)
                
        with storeFactory.store() as store:
            store.updateJobStatus(jobId, JOB_DELETE)
        #删除缓存让下一个task可以同名
        tasks=CacheHolder.getCache().get(jobId, JOBS).tasks
        for taskName in tasks:
            if TaskCacheHolder.getJobCache().has_key(taskName):
                TaskCacheHolder.getJobCache().remove(taskName)
        
        CacheHolder.getCache().remove(jobId, JOBS)
    except:
        Logger.exception(log)

def jobAuditStatusHandler(event):
    jobId = event.jobId
    status = event.status
    with storeFactory.store() as store:
        store.updateAuditStatus(jobId,status)

def runJob(job,params):
    
    t = job.fileType
    jobId =job.jobId
    jobRun =  JobCacheHolder.getJobCache().get(jobId)
    if not jobRun:
        jobRun = JobHolder.getJob(t)(job)
        JobCacheHolder.getJobCache().put(jobId,jobRun)
    
    jobRun.start(params)
    
def checkAllWorkBeReady(job):
    jobId=job.jobId
    with storeFactory.store() as store:
        readyWorks = store.getJobWorksReadyDone(jobId)
    notReadyWorks =[]
    isAllBeReady = True
    for work in job.works:
        hostName = work.hostName
        if hostName not in readyWorks:
            notReadyWorks.append(hostName)
            isAllBeReady=False
    
    return (isAllBeReady,notReadyWorks)
    
def jobRunHandler(event):
    jobId = event.jobId
    params = event.params
    ignoreNotPerWork = event.ignoreNotPerWork
    
    if not CacheHolder.getCache().hasKey(jobId, JOBS):
        with storeFactory.store() as store:
            job=store.getJob(jobId)
            CacheHolder.getCache().put(jobId, job,JOBS)
    else:
        job = CacheHolder.getCache().get(jobId,JOBS)
    if ignoreNotPerWork:
        runJob(job,params)
    else:
        (isAllBeReady,works)=checkAllWorkBeReady(job)
        if isAllBeReady:
            runJob(job,params)
        else:
            raise Exception("works:%s not be ready"% ",".join(works))
        
        

    
    
    