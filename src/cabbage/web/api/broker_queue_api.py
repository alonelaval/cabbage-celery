# -*- encoding: utf-8 -*-
'''
Created on 2016年8月31日

@author: huawei
'''
from cabbage.common.Kombu.kombu_amqp_client import KombuClient
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.constants import JOBS, JOB_DELETE
from cabbage.data.entity import BrokerQueue
from cabbage.web.api.job_api import JobApi
from cabbage.web.api.util import excute
from cabbage.web.api.work_api import WorkApi
# from cabbage.data.store_holder import StoreHolder

class BrokerQueueApi(object):
    
    @excute
    def addQueueNode(self,store,brokerQueue,nodes):
        brokerQueueEntity = self.getQueueByName( brokerQueue)
        
        works=[] 
        workApi=WorkApi()
        for n in nodes:
            hostname=n.split(":")[0]
            work = workApi.getWork(hostname)
            if work.brokerServer != ""  and  work.brokerServer != brokerQueueEntity.server:
                raise Exception("队列集群不对！")
            
            works.append(work)
        
        #添加job worker
        jobApi = JobApi()
        jobs = jobApi.getCacheJobs()
        for job in jobs:
            if job.brokerServer==brokerQueueEntity.server and job.brokerQueue == brokerQueueEntity.queueName:
                for work in works:
                    jobApi.addJobWork(job.jobId, work)
        #添加queue worker信息
        #添加worker信息
        for work in works:
            store.addQueueWork(brokerQueueEntity,work)
            workApi.addWorkQueue(brokerQueueEntity, work)
        
    @excute
    def removeQueueNode(self,store,brokerQueue,nodes):
        brokerQueueEntity = self.getQueueByName( brokerQueue)
        
        works=[] 
        workApi=WorkApi()
        nodeHostNames=[]
        for n in nodes:
            hostname=n.split(":")[0]
            nodeHostNames.append(hostname)
            work = workApi.getWork(hostname)
            if work.brokerServer != brokerQueueEntity.server:
                raise Exception("队列集群不对！")
             
            works.append(work)
#         
#         #移除job worker
        jobApi = JobApi()
        jobs = jobApi.getCacheJobs()
        
        for job in jobs:
            if job.brokerServer==brokerQueueEntity.server and job.brokerQueue == brokerQueueEntity.queueName:
                workLen = len(job.works)
                
                for jw in job.works:
                    if jw.hostName in nodeHostNames:
                        workLen = 1
                        
                
                pass
            
            
            
#                 for work in works:
#                     jobApi.addJobWork(job.jobId, work)
                
#            #添加queue worker信息
            #添加worker信息
#         for work in works:
#             store.addQueueWork(brokerQueueEntity,work)
#             workApi.addWorkQueue(brokerQueueEntity, work)
       
    
    @excute
    def getBrokerQueue(self,store):
        return store.getQueues()
    @excute
    def getQueueByName(self,store,queueName):
        return store.getQueue(queueName)
    @excute
    def isExistQueueName(self,store,queueName):
        return store.isExistQueue(queueName)
    @excute
    def addQueue(self,store,brokerServer,brokerQueue,exchange,routingKey,nodes):
        exchange = exchange if exchange else brokerQueue
        routingKey = routingKey if routingKey else brokerQueue
        workApi=WorkApi()
        works =[]
        if nodes and nodes[0] == "-1":
                works =workApi.getWorks()
        elif nodes: 
            for node in nodes:
                workName = node.split(":")[0]
                works.append(workApi.getWork(workName))
        else:
            works =workApi.getWorks()
      
        brokerServer=brokerServer.split(":")[0]
        server =  store.getBrokerServer(brokerServer)
        client = KombuClient(url=server.connectUri)
        client.addQueue(brokerQueue,exchangeName=exchange,routingKey=routingKey)
        queue  = BrokerQueue(server=brokerServer,queueName=brokerQueue,exchangeName=exchange,routingKey=routingKey,works=[work.hostName for work in works])
        
        store.saveQueue(queue)
        store.addServerBrokerQueue(server, queue)
        
        queues = {}
        
        for work in works:
            jobIds =store.getJobIds()
            for jobId in jobIds:
                job = CacheHolder.getCache().get(jobId, JOBS)
                workIsRun = False
                for w in job.works :
                    if work.hostName == w.hostName and job.status != JOB_DELETE:
                        workIsRun =True
                        
                if work.brokerServer != brokerServer and workIsRun:
                    raise Exception("有未删除的JOB【%s】在使用该节点，导致节点无法切换服务器,添加队列失败！"%job.jobId)
                
            if  work.brokerServer != brokerServer:
                for q in work.queues:
                    if q in queues:
                        queues[q] =queues[q]+[work.hostName]
                    else:
                        queues[q] =[work.hostName]
                
            
            store.addWorkBrokerServerBrokerQueue(work, brokerServer, brokerQueue)
        
        
        
        for key,values in queues.items():
            for v in values:
                store.removeWorkFromQueue(key, str(v))
        
        
        
        
        
        
        
            
        
        
        
        
        
        
        
        
        
        
