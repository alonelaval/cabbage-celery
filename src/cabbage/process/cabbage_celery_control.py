# -*- encoding: utf-8 -*-
'''
Created on 2016年7月25日

@author: huawei
'''
from cabbage.cabbage_celery import celeryconfig
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.cabbage_celery.util import isCabbageTask
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.file.load_file_holder import LoadMoudleHolder
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, CLIENT_FILE_DIRECTORY, PYTHON, JOB_DELETE, \
    JOBS
from cabbage.data.store_holder import StoreHolder
from cabbage.event.handler.client_job_audit_pass_handler import syncJob, \
    syncFile
from cabbage.message.file_message import FileRequestMessage
from cabbage.utils.host_name import HOST_NAME
from cabbage.utils.util import singleton
import multiprocessing
import os
import threading
import time
from kombu.entity import Exchange, Queue

log = Logger.getLogger(__name__)

@singleton
class CabbageControl():
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.jobQueue =self.manager.Queue()
        #控制器
        
    def _initJobs(self,cabbage):
        store = StoreHolder.getRetryStore()
        jobs =store.getJobs()
        work =store.getWork(HOST_NAME)
        queues=work.queues
        routes={}
        queues_celery=[]
        for que in queues:
            que= store.getQueue(que)
            queues_celery.append(Queue(que.queueName, Exchange(que.queueName), routing_key=que.queueName,queue_arguments={'x-max-priority':int(que.priority)}))
            
        for job in jobs:
            if job.status != JOB_DELETE  and job.brokerQueue in queues:

                #fixbug 动态扩容时，缓存JOB
                if not CacheHolder.getCache().hasKey(job.jobId, JOBS):
                    CacheHolder.getCache().put(job.jobId, job,JOBS)
                
                clientDir = ConfigHolder.getConfig().getProperty(BASE,CLIENT_FILE_DIRECTORY)
                path = clientDir+"/"+job.jobId  
                if not os.path.isdir(path) :
                    # @FIX BUG  文件不同步
                    syncJob(job.jobId,store)

                self.addScriptJobId(job.jobId,cabbage)
                
                for taskName in job.tasks:
                    que= store.getQueue(job.brokerQueue)
                    routes[taskName]={'queue': que.queueName, 'routing_key': que.routingKey}
       
        log.info(routes);
        celeryconfig.CELERY_QUEUES = tuple(queues_celery)
        celeryconfig.CELERY_ROUTES = routes
        
        
    def startCelery(self):
       
        self.cabbage = CabbageHolder.getCabbage()
        
        def run(cabbage):
            cabbage.start()
            
        def start():
            #使用子进程，加载任务，类沙箱的概念
            cabbage =CabbageHolder.getCabbage()
            self._initJobs(cabbage)
            t1 = threading.Thread(target=run,args=(cabbage,))
            t1.setDaemon(True)
            t1.start()
            t1.join()
            
        p2 = multiprocessing.Process(target = start)
        p2.start()
        p2.join()
    
    def _restart(self,hostName=HOST_NAME):
        try:
            if self.cabbage.workIsAlive(hostName):
                self.stopCelery()
            time.sleep(5)
            self.startCelery()
        except:
            self.startCelery()
            
    def restartCelery(self):
        t1 = threading.Thread(target=self._restart)
        t1.setDaemon(True)
        t1.start()

    def stopCelery(self,hostName=HOST_NAME):
        try:
            if self.cabbage.workIsAlive(hostName):
                self.cabbage.stop(hostName)
        except:
            pass
        
    def addScriptJobId(self,jobId,cabbage):
        store =None
        try:
            store = StoreHolder.getStore()
            log.info("节点【%s】当前任务【%s】的脚本开始加载。。。。" % (HOST_NAME,jobId))
            self.loadJobScript(jobId,store,cabbage)
            work=store.getWork(HOST_NAME)
            self.sendBeReady(jobId,work,store)
            store.close()
        except Exception:
            Logger.exception(log)
        finally:
            if store:
                store.close()
    
    def loadJobScript(self,jobId,store,cabbage):
        '''
            将当前任务的脚本准备好
        '''
        job=store.getJob(jobId)
        
        clientDir = ConfigHolder.getConfig().getProperty(BASE,CLIENT_FILE_DIRECTORY)
        path = clientDir+"/"+jobId
        #不同步主节点文件
#         if job.fileType == PYTHON:
#             if not os.path.isfile(path+"/"+job.fileName):
#                 syncFile(job.fileName,jobId,FileRequestMessage.MAIN)
#             self.loadCeleryTask(path,job.fileName)
            
        if job.attachFiles: 
            for attachFile in job.attachFiles:
                if attachFile.fileType == PYTHON:
                    if not os.path.isfile(path+"/"+attachFile.fileName):
                        syncFile(attachFile.fileName,jobId,FileRequestMessage.ATTACH)
                    self.loadCeleryTask(path,attachFile.fileName,cabbage)
        log.info("节点【%s】当前任务【%s】的脚本加载完" % (HOST_NAME,jobId))
        
    def loadCeleryTask(self,path,fileName,cabbage):
        loadMoudle = LoadMoudleHolder.getLoadMoudle(PYTHON)
        classes = loadMoudle.load(path,fileName)
        for key,value in classes:
            if isCabbageTask(value):
                cabbage.register_task(value())
                       
    
    def sendBeReady(self,jobId,work,store):
        '''
            发送当前节点的关于当前任务的状态为已经准备好
        '''
        store.updateJobWorkReady(jobId, work)
        log.info("节点【%s】当前任务【%s】节点已经准备完毕" % (HOST_NAME,jobId))
    

    