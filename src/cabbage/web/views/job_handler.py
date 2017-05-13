# -*- encoding: utf-8 -*-
'''
Created on 2016年7月29日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.constants import JOB_DELETE
from cabbage.event.server_jobs_event import JobRunEvent
#     JobUpdateEvent, JobRemoveEvent
# from cabbage.process.cabbage_job_excutor import \
#     CabbageJobExecutorHolder, CabbageJobExecutor
# from cabbage.queue.job_queue import JobEventPoolHolder
from cabbage.web.api.job_api import JobApi
# from cabbage.web.api.work_api import WorkApi
from cabbage.web.views.base_handler import BaseHandler
from concurrent import futures
from tornado import gen
# import os
# import threading
# import time
import tornado
import zope.event

log = Logger.getLogger(__name__)

        
class JobListDataHandler(BaseHandler):
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
    def get(self):
        self.render("job_list.html")
        
class RemoveJobListHandlder(BaseHandler):
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
    
    def get(self):
        self.render("run_job.html")
        
    def _runJob(self,event):
        zope.event.notify(event)
        
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
        
#         CabbageJobExecutorHolder.getCabbageJobExecutor().addJobEvent(JobRunEvent(jobId,params))
        
#         zope.event.notify(JobRunEvent(jobId,params))
#         from cabbage.server_start import CabbageServerHolder
#         if CabbageServerHolder.getServer().status != ON_LINE:
#             self.write("系统还没有初始化好！")        
#             return
        
#         yield tornado.gen.Task(self._runJob,JobRunEvent(jobId,params))
        tornado.ioloop.IOLoop.instance().add_callback(self._runJob,JobRunEvent(jobId,params))
        #CabbageJobExecutorHolder.getCabbageJobExecutor().addJobEvent(JobRunEvent(jobId,params))
        
#         runJob = def __runJob(self,evnet):
#                     zope.event.notify(evnet)
            
#         JobRunHandler.executor.submit(__runJob,JobRunEvent(jobId,params))
#         t2 = threading.Thread(target=self.__runJob,args=(JobRunEvent(jobId,params),))
#         t2.setDaemon(True)
#         t2.start()
        
        
#         JobEventPoolHolder.getJobEventPool().add(JobRunEvent(jobId,params))
        
