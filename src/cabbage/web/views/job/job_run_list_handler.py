# -*- encoding: utf-8 -*-
'''
Created on 2016年8月24日

@author: huawei
'''
from cabbage.web.api.job_api import JobApi
from cabbage.web.views.base_handler import BaseHandler
import json
import tornado
class JobRunListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("run_job_list.html")
    @tornado.web.authenticated
    def post(self):
        jobApi= JobApi()
        jobMoniotrs =jobApi.getRunJobs()
        if jobMoniotrs:
            jobList= []
            for jobMonitor in jobMoniotrs:
                jobId = jobMonitor.jobId
                job = jobApi.getJobByJobId(jobId)
                #taskCount,taskSucceeded,taskFailed,taskRuntime,taskQueueTime
                jobApi.getJobByJobId(jobId)
                
                d =  {"jobId":jobMonitor.jobId,
                     "jobName":job.jobName,
#                      "fileName":job.fileName,
                     "fileType":job.fileType,
                     "queue":job.brokerQueue,
                     "taskCount":jobMonitor.taskCount,
                     "taskSucceeded":jobMonitor.taskSucceeded,
                     "taskFailed":jobMonitor.taskFailed,
                     "taskRuntime":jobMonitor.taskRuntime,
                     "taskReceived":jobMonitor.taskReceived,
                     "taskQueueTime":jobMonitor.taskQueueTime
                     }
                jobList.append(d)
                
            self.write( json.dumps(jobList))
               
        
        