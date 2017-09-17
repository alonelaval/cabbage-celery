# -*- encoding: utf-8 -*-
'''
Created on 2016年7月29日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.constants import JOB_DELETE
from cabbage.event.server_jobs_event import JobRunEvent
from cabbage.web.api.job_api import JobApi
from cabbage.web.views.base_handler import BaseHandler
from concurrent import futures
from tornado import gen
import tornado
import zope.event
#     JobUpdateEvent, JobRemoveEvent
# from cabbage.process.cabbage_job_excutor import \
#     CabbageJobExecutorHolder, CabbageJobExecutor
# from cabbage.queue.job_queue import JobEventPoolHolder
# from cabbage.web.api.work_api import WorkApi
# import os
# import threading
# import time

log = Logger.getLogger(__name__)

        
class JobListDataHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        limit = self.getArgument("limit")
        offset = self.getArgument("offset")
        (jobs,totalCount) = JobApi().getJobByPage(int(limit), int(offset))
        
        m ={}
        m["total"]=totalCount
        da=[]
        for d in jobs:
#             if d ==READIES:
#                 continue 
            da.append({"jobId":d.jobId,
                       "jobName":d.jobName,
                       "fileName":d.fileName,
                       "fileType":d.fileType,
                       "status":d.status,
                       "works":[w.hostName for w in d.works],
                       "brokerServer":d.brokerServer,
                       "brokerQueue":d.brokerQueue,
                       
            })
        m["rows"]=da
        self.write(m)

class JobListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("job_list.html")
        
class RemoveJobListHandlder(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        jobId = self.getArgument("jobId")
        if not jobId or jobId=="":
            self.write("jobId不能为空！")
            return
        job = JobApi().getJobByJobId(jobId)  #CacheHolder.getCache().hasKey(jobId, JOBS)
        if job is None:
            self.write("jod【%s】找不到！"%jobId)        
            return
        if job.status ==JOB_DELETE:
            self.write("jod【%s】已删除！"%jobId)        
            return
            
        JobApi().removeJob(jobId)
       
        
# def __runJob(evnet):
#     zope.event.notify(evnet)
#         
class JobRunHandler(BaseHandler):
    
    executor =  futures.ThreadPoolExecutor(max_workers=2000)
    
#     cabbageJobExecutor = CabbageJobExecutor()
    @tornado.web.authenticated
    def get(self):
        self.render("run_job.html")
        
    def _runJob(self,event):
        zope.event.notify(event)
    
#     @tornado.web.authenticated    
    @gen.coroutine
    def post(self):
        jobId = self.getArgument("jobId")
        params = self.getArgument("params")
        if not jobId or jobId=="":
            self.write("jobId不能为空！")
            return
        job = JobApi().getJobByJobId(jobId) #CacheHolder.getCache().get(jobId, JOBS)
        if not job or job.status == JOB_DELETE:
            self.write("jod【%s】找不到！"%jobId)        
            return
        
        tornado.ioloop.IOLoop.instance().add_callback(self._runJob,JobRunEvent(jobId,params))
