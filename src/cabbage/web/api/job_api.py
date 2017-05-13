# -*- encoding: utf-8 -*-
'''
Created on 2016年8月4日

@author: hua
'''
from cabbage.common.cabbage_celery.util import isCabbageTask
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.file.load_file_holder import LoadMoudleHolder
from cabbage.config import ConfigHolder
from cabbage.constants import JOBS, BASE, SERVER_FILE_DIRECTORY, \
    PYTHON
# from cabbage.data.store_holder import StoreHolder
from cabbage.event.server_jobs_event import JobRemoveEvent
# from cabbage.job.job_cache import JobCacheHolder
from cabbage.web.api.util import excute
# import os
import zope.event
class JobApi(object):
    @excute
    def saveJob(self,store,job):
        store.saveJob(job)
        
    @excute
    def addJobWork(self,store,jobId,work):
        store.addJobWork(jobId,work)
        
    def getCacheJobs(self):
        jobIds = CacheHolder.getCache().getRegion(JOBS).namespace.keys()
        jobs = []
        for jobId in jobIds:
            jobs.append(CacheHolder.getCache().get(jobId, JOBS))
            
        return jobs
    
    @excute
    def getJobByPage(self,store,limit,offset):
        jobIds = store.getJobIds()
        totalCount = len(jobIds)
        ids = jobIds[offset:offset+limit]
        jobs = []
        for jobId in ids:
#             jobs.append(CacheHolder.getCache().get(jobId, JOBS))
            job = store.getJob(jobId)
            jobs.append(job)
            CacheHolder.getCache().put(jobId,job,JOBS)
            
        return (jobs,totalCount)
    @excute
    def getRunJobs(self,store):
        return store.getJobMonitors()
        
        
#         return JobCacheHolder.getJobCache().values()
    
    def removeJob(self,jobId):
        zope.event.notify(JobRemoveEvent(jobId))
         
    @excute
    def getJobByJobId(self,store,jobId):
        if not CacheHolder.getCache().hasKey(jobId, JOBS):
            return None
        else:
            return  CacheHolder.getCache().get(jobId, JOBS)
            
    
    def getTasks(self,fileName,jobId):
        serverDir = ConfigHolder.getConfig().getProperty(BASE,SERVER_FILE_DIRECTORY)
        path = serverDir+"/"+jobId
        loadMoudle = LoadMoudleHolder.getLoadMoudle(PYTHON)
        classes =loadMoudle.load(path,fileName)
        tasks=[]
        for clazz in classes:
            cls = clazz[1]
            if isCabbageTask(cls):
                tasks.append(cls.__module__  +"."+ cls.__name__)
        return tasks