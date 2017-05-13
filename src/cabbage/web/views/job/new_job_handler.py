# -*- encoding: utf-8 -*-
'''
Created on 2016年8月31日

@author: huawei
'''
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, SERVER_FILE_DIRECTORY, PYTHON, \
    JOB_AUTH_PASS, OFF_LINE
from cabbage.data.entity import Job, File
from cabbage.event.server_jobs_event import JobAuditEvent
from cabbage.web.api.broker_queue_api import BrokerQueueApi
from cabbage.web.api.broker_server_api import BrokerServerApi
from cabbage.web.api.job_api import JobApi
from cabbage.web.api.work_api import WorkApi
from cabbage.web.views.base_handler import BaseHandler
import os
import time
import zope.event
log = Logger.getLogger(__name__)

class NewJobHandler(BaseHandler):
    python_type=u"text/x-python-script"
    def get(self):
        self.render("new_job.html",works=WorkApi().getWorks(),servers=BrokerServerApi().getBrokerServers())
        
    def post(self):
        try:
            jobName= self.getArgument("jobName")
            
         
            serverDir = ConfigHolder.getConfig().getProperty(BASE,SERVER_FILE_DIRECTORY)
            
            proType = self.getArgument("proType")
            params = self.getArgument("params")
            runStrategy = self.getArgument("runStrategy")
            strategyValue = self.getArgument("strategyValue")
            brokerServer = self.getArgument("brokerServer")
            brokerQueue = self.getArgument("brokerQueue")
            resultBackend = self.getArgument("resultBackend")
            
            if jobName is None  or "mainFile" not in self.request.files or brokerServer is None or brokerQueue is None:
                raise Exception("参数不能为空！")
                return
            
            log.debug(params)
            jobName = str(jobName)
            proType=str(proType)
            
           
            job=Job(jobName=str(jobName),fileType=proType)
            job.runStrategy=str(runStrategy)
            job.strategyValue = str(strategyValue)
            job.brokerServer = brokerServer
            job.brokerQueue = brokerQueue
            
            jobApi= JobApi()
            
            mainFile = self.request.files['mainFile'][0]
            works =[]
            os.mkdir(serverDir+"/"+job.jobId) 
            os.mkdir(serverDir+"/"+job.jobId+"/result") 
            if mainFile:
                fileName=mainFile['filename']
                fileName=str(fileName)
                body = mainFile['body']
                p = serverDir+"/"+job.jobId+"/"+fileName
                fn = open(p,"w")
                fn.write(body)
                fn.close()
                job.filePath=p
                job.fileName=fileName
            
            
            nodes = BrokerQueueApi().getQueueByName(brokerQueue).works
            
            if nodes is None  or len(nodes) ==0 :
                raise Exception("【%s】队列没有添加执行节点！"%brokerQueue)
            
            workApi=WorkApi()
            if nodes and nodes[0] == "-1":
                works =WorkApi().getWorks()
            elif nodes: 
                for node in nodes:
                    works.append(workApi.getWork(node))
            else:
                works =WorkApi().getWorks()
                
            attachFiles = []
            
            job.works=works
            
            tasks = []
            for attachFile in self.request.files['attachs']:
                log.debug(attachFile)
                fileName=attachFile['filename']
                fileName=str(fileName)
                body = attachFile['body']
                
                
                fileType=PYTHON if attachFile['content_type'] == NewJobHandler.python_type or fileName.endswith(".py") else "text"
                
                p = serverDir+"/"+job.jobId+"/"+fileName
                fn = open(p,"w")
                fn.write(body)
                fn.close()
                
                
                attachFiles.append(File(fileName=fileName,jobId=job.jobId,jobName=job.jobName,filePath=p,fileType=fileType))
                
            for attachFile in attachFiles:
                if attachFile.fileType == PYTHON:
                    tasks += jobApi.getTasks(attachFile.fileName, job.jobId)
                
                
            job.attachFiles=attachFiles
            job.status=JOB_AUTH_PASS
            job.tasks = tasks
            job.resultBackend=resultBackend.lower()
            log.debug(works)
            
            jobApi.saveJob(job)
            time.sleep(5)
            
            for work in works:
                WorkApi().workChangeStatus(work, OFF_LINE)
            
            zope.event.notify(JobAuditEvent(job.jobId,JOB_AUTH_PASS))
            
            self.write(job.jobId)
        except Exception as e:
            log.exception(e)
            self.render("new_job.html",works=WorkApi().getWorks(),servers=BrokerServerApi().getBrokerServers(),errorMessage="添加任务失败，原因：%s！" % str(e))
            
#         time.sleep(15)
#         zope.event.notify(JobRunEvent(job.jobId))