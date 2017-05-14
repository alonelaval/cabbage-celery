# -*- encoding: utf-8 -*-
'''
Created on 2016年6月8日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.constants import CABBAGE, JOBS, JOB_NAME, FILE_PATH, FILE_NAME, \
    FILE_TYPE, STATUS, AUDIT_STATUS, RUN_STRATEGY, ATTACH_FILES, WORKS, FILES, \
    JOB_ID, AUTHS, AUDIT_USER, AUDIT_TIME, USER_PWD, IS_ADMIN, USERS, LIST, READIES, \
    PORT, IP, DONE, STRATEGY_VALUE, QUEUE_SERVER, QUEUES, EXCHANGE, ROUTING_KEY, \
    SERVER, BROKER_SERVERS, CONNECT_URI, SERVER_TYPE, BROKER_SERVER, QUEUE, TASKS, \
    DO_SOMETHING, DO_NOTHING, MONITOR, TASK_COUNT, TASK_SUCCEEDED, TASK_FAILED, \
    TASK_RUNTIME, DATES, TASK_QUEUE_TIME, CONFIG, DESC, REULST_BACKEND, RESULTS, \
    SERVICE_STATUS, TASK_RECEIVED
from cabbage.data.entity import File, Work, Job, Auth, User, BrokerQueue, \
    BrokerServer, TaskMonitor, JobMonitor, WorkMonitor, DateMonitor, BrokerMonitor, \
    Config
from cabbage.data.store import Store
from kazoo.retry import KazooRetry
from zope.interface.declarations import implementer
import time
import zope.event
# from cabbage.utils.util import singleton
log = Logger.getLogger(__name__)
# @singleton
@implementer(Store)
class ZookeeperStore(object):
         
    def __init__(self,isRetry=False):
        if isRetry:
            self.client = ZookeeperClientHolder.getRetryClient()
        else:
            self.client= ZookeeperClientHolder.getClient()
    
    def isConnected(self):
        return self.client.isConnected()
    def close(self):
        self.client.close()
    def state(self):
        return self.client.state()
    def saveJob(self,job):
        parent="/"+CABBAGE+"/"+JOBS+"/"+job.jobId
        self.client.create(parent,makepath=True)
        Logger.debug(log,parent)
        self.client.create(parent+"/"+JOB_NAME, value=job.jobName)
        self.client.create(parent+"/"+FILE_PATH,  value=job.filePath)
        self.client.create(parent+"/"+FILE_NAME, value=job.fileName)
        self.client.create(parent+"/"+FILE_TYPE,  value=job.fileType)
        self.client.create(parent+"/"+STATUS, value=job.status)
        self.client.create(parent+"/"+AUDIT_STATUS,  value=job.auditStatus)
        self.client.create(parent+"/"+RUN_STRATEGY,  value=job.runStrategy)
        self.client.create(parent+"/"+STRATEGY_VALUE,  value=job.strategyValue)
        self.client.create(parent+"/"+ATTACH_FILES)
        self.client.create(parent+"/"+REULST_BACKEND, value=job.resultBackend)
        for f in job.attachFiles:
            self.client.create(parent+"/"+ATTACH_FILES+"/"+f.fileName,value=f.filePath,makepath=True)
            self.client.create(parent+"/"+ATTACH_FILES+"/"+f.fileName+"/"+FILE_TYPE,value=f.fileType,makepath=True)
        for w in job.works:
            self.client.create(parent+"/"+WORKS+"/"+LIST+"/"+w.hostName,value=w.port,makepath=True)
            if not self.client.isExistPath(parent+"/"+WORKS+"/"+READIES):
                self.client.create(parent+"/"+WORKS+"/"+READIES)
        
        
        if job.tasks:
            for task in job.tasks:
                self.client.create(parent+"/"+TASKS+"/"+task,makepath=True)
                self.client.create("/"+CABBAGE+"/"+JOBS+"/"+RESULTS+"/"+job.jobId+"/"+task,makepath=True)
        
        self.client.create(parent+"/"+BROKER_SERVER, value=job.brokerServer)
        
        self.client.create(parent+"/"+QUEUE,value=job.brokerQueue)
        
#         for q in job.queue:
#             self.client.create(parent+"/"+BROKER_SERVER+"/"+QUEUES+"/"+q)
                
        #使用该目录是因为，如果前面的目录没有创建完，集群的节点已经开始监控，导致数据不完整，所以，单独才用该目录来进行节点的监控
        self.client.create("/"+CABBAGE+"/"+JOBS+"/"+READIES+"/"+job.jobId)
            
    def getJobs(self):
        parent="/"+CABBAGE+"/"+JOBS
        jobIds = self.client.getChildren(parent)
        jobs=[]
        for jobId in jobIds:
            if jobId ==READIES or jobId == RESULTS:
                continue 
            
            jobs.append(self.getJob(jobId))
        return jobs
    
    
    def getJobIds(self):
        parent="/"+CABBAGE+"/"+JOBS
        jobIds = self.client.getChildren(parent)
        jobIds.remove(READIES)
        if RESULTS in jobIds: 
            jobIds.remove(RESULTS)
        return jobIds
    def updateJobStatus(self,jobId,jobStatus):
        parent="/"+CABBAGE+"/"+JOBS+"/"+jobId
        self.client.putData(parent+"/"+STATUS,jobStatus)
#         from cabbage.event.server_jobs_event import JobUpdateEvent
#         zope.event.notify(JobUpdateEvent(jobId))
        
    def updateJobWorkReady(self,jobId,work):
        self.removeJobWorkReady(jobId,work)
        parent="/"+CABBAGE+"/"+JOBS+"/"+jobId
        self.client.create(parent+"/"+WORKS+"/"+READIES+"/"+work.hostName,value=DONE,makepath=True)
#         from cabbage.event.server_jobs_event import JobUpdateEvent
#         zope.event.notify(JobUpdateEvent(jobId))


    def removeJobWorkReady(self,jobId,work):
        path="/"+CABBAGE+"/"+JOBS+"/"+jobId+"/"+WORKS+"/"+READIES+"/"+work.hostName
        if self.client.isExistPath(path):
            self.client.delete(path)
            
    def getJobWorksReadyDone(self,jobId):
        parent="/"+CABBAGE+"/"+JOBS+"/"+jobId+"/"+WORKS+"/"+READIES+"/"
        return self.client.getChildren(parent)
    
    def updateAuditStatus(self,jobId,auditStatus):
        parent="/"+CABBAGE+"/"+JOBS+"/"+jobId
        self.client.putData(parent+"/"+AUDIT_STATUS, auditStatus)
        from cabbage.event.server_jobs_event import JobUpdateEvent
        zope.event.notify(JobUpdateEvent(jobId))
            
    def getJob(self,jobId):
        parent="/"+CABBAGE+"/"+JOBS+"/"+jobId
#         log.debug(self.client)
        jobName= self.client.getData(parent+"/"+JOB_NAME)
        log.debug(parent)
        filePath = self.client.getData(parent+"/"+FILE_PATH)
        fileName = self.client.getData(parent+"/"+FILE_NAME)
        fileType = self.client.getData(parent+"/"+FILE_TYPE)
        status  = self.client.getData(parent+"/"+STATUS)
        auditStatus = self.client.getData(parent+"/"+AUDIT_STATUS)
        runStrategy = self.client.getData(parent+"/"+RUN_STRATEGY)
        resultBackend=None
        if self.client.isExistPath(parent+"/"+REULST_BACKEND):
            resultBackend = self.client.getData(parent+"/"+REULST_BACKEND)
        
        files = self.client.getChildren(parent+"/"+ATTACH_FILES)
        log.debug(parent+"/"+WORKS+"/"+LIST)
        ws = self.client.getChildren(parent+"/"+WORKS+"/"+LIST)
        attachFiles = []
        works = []
        for attachFile in files:
            fp = self.client.getData(parent+"/"+ATTACH_FILES+"/"+attachFile)
            ft = self.client.getData(parent+"/"+ATTACH_FILES+"/"+attachFile+"/"+FILE_TYPE)
            f = File(fileName=attachFile,filePath=fp,fileType=ft)
            attachFiles.append(f)
        for  w in ws:
            pt = self.client.getData(parent+"/"+WORKS+"/"+LIST+"/"+w)
            works.append(Work(hostName=w,port=pt))
            
        tasks = []
        if self.client.isExistPath(parent+"/"+TASKS):
            tasks = self.client.getChildren(parent+"/"+TASKS) 
               
                 
        brokerServer =  None
        brokerQueue = None
        if self.client.isExistPath(parent+"/"+BROKER_SERVER):
            brokerServer = self.client.getData(parent+"/"+BROKER_SERVER)
            
        if self.client.isExistPath(parent+"/"+QUEUE):
            brokerQueue = self.client.getData(parent+"/"+QUEUE)
        
        return Job(jobId=jobId,jobName=jobName,filePath=filePath,status=status,auditStatus=auditStatus,
             fileType=fileType,fileName=fileName,attachFiles=attachFiles,works=works,runStrategy=runStrategy,
             brokerServer=brokerServer,brokerQueue=brokerQueue,tasks=tasks,resultBackend=resultBackend)
    
    def saveFile(self,f):
        parent="/"+CABBAGE+"/"+FILES
        self.client.create(parent+"/"+f.fileName,makepath=True)
        self.client.create(parent+"/"+f.fileName+"/"+JOB_ID, value=f.jobId)
        self.client.create(parent+"/"+f.fileName+"/"+JOB_NAME, value=f.jobName)
        self.client.create(parent+"/"+f.fileName+"/"+FILE_PATH, value=f.filePath)
        self.client.create(parent+"/"+f.fileName+"/"+FILE_TYPE, value=f.fileType)
        
    def getFiles(self):
        parent="/"+CABBAGE+"/"+FILES
        fileNames = self.client.getChildren(parent)
        files = []
        for fileName in fileNames:
            files.append(self.getFile(fileName))
        return files
    
    def getFile(self,fileName):
        parent="/"+CABBAGE+"/"+FILES
        jobId = self.client.getData(parent+"/"+fileName+"/"+JOB_ID)
        jobName = self.client.getData(parent+"/"+fileName+"/"+JOB_NAME)
        filePath = self.client.getData(parent+"/"+fileName+"/"+FILE_PATH)
        fileType = self.client.getData(parent+"/"+fileName+"/"+FILE_TYPE)
        return File(fileName=jobName,jobId=jobId,jobName=jobName,filePath=filePath,
                 fileType=fileType)
    
    def saveAuth(self,auth):
        parent="/"+CABBAGE+"/"+AUTHS+"/"+auth.jobId
        self.client.create(parent,makepath=True)
        self.client.create(parent+"/"+AUDIT_USER, value = auth.auditUser)
        self.client.create(parent+"/"+AUDIT_TIME, value = auth.auditTime)
        self.client.create(parent+"/"+AUDIT_STATUS, value = auth.auditStauts)

    def getAuths(self):
        parent="/"+CABBAGE+"/"+AUTHS
        ids = self.client.getChildren(parent)
        auths = []
        for jobid in ids:
            auths.append(self.getAuth(jobid))
        return auths
        
    def getAuth(self,jobId):
        parent="/"+CABBAGE+"/"+AUTHS+"/"+jobId
        auditUser = self.client.getData(parent+"/"+AUDIT_USER)
        auditTime = self.client.getData(parent+"/"+AUDIT_TIME)
        auditStatus = self.client.getData(parent+"/"+AUDIT_STATUS)
        return Auth(jobId=jobId,auditUser=auditUser,auditStauts=auditStatus,auditTime=float(auditTime))
    
    def saveUser(self,user):
        parent="/"+CABBAGE+"/"+USERS+"/"+user.userName
        self.client.create(parent,makepath=True)
        self.client.create(parent+"/"+USER_PWD, value = user.userPwd)
        self.client.create(parent+"/"+IS_ADMIN, value = "1" if user.isAdmin else "0")
        
    def getUsers(self):
        parent="/"+CABBAGE+"/"+USERS
        names = self.client.getChildren(parent)
        users = []
        for userName in names:
            users.append(self.getUser(userName))
        return users
        
    def getUser(self,userName):
        parent="/"+CABBAGE+"/"+USERS+"/"+userName
        if self.client.isExistPath(parent):
            userPwd =  self.client.getData(parent+"/"+USER_PWD)
            isAdmin = self.client.getData(parent+"/"+IS_ADMIN)
            isAdmin  = True if isAdmin =='1' else False
            return User( userName=userName,userPwd=userPwd,isAdmin=bool(isAdmin))
        return None
    
    def getWork(self,hostName):
        parent="/"+CABBAGE+"/"+WORKS+"/"+hostName
        port = self.client.getData(parent+"/"+PORT)
        ip   = self.client.getData(parent+"/"+IP)
        status =self.client.getData(parent+"/"+STATUS)
        
        brokerServer =  None
        serviceStatus =None
        queues= []
        if self.client.isExistPath(parent+"/"+BROKER_SERVER):
            brokerServer = self.client.getData(parent+"/"+BROKER_SERVER)
            
        if self.client.isExistPath(parent+"/"+SERVICE_STATUS):
            serviceStatus = self.client.getData(parent+"/"+SERVICE_STATUS)
            
        if self.client.isExistPath(parent+"/"+QUEUES):
            queues = self.client.getChildren(parent+"/"+QUEUES)
            
        return  Work(port=port,ip=ip,status=status,hostName=hostName,brokerServer=brokerServer,queues=queues,serviceStatus=serviceStatus)
    
    def isExistWork(self,work):
        parent="/"+CABBAGE+"/"+WORKS+"/"+work.hostName
        return self.client.isExistPath(parent)
    
    def getWorks(self):
        parent="/"+CABBAGE+"/"+WORKS
        workNames = self.client.getChildren(parent)
        works = []
        for workName in workNames:
            if workName ==READIES:
                continue 
            works.append(self.getWork(workName))
        
        return works
    
    def saveWork(self,work):
        parent="/"+CABBAGE+"/"+WORKS+"/"+work.hostName
        if self.client.isExistPath(parent):
            self.client.delete(parent,recursive=True)
            
        self.client.create(parent,makepath=True)
        self.client.create(parent+"/"+IP, value = work.ip)
        self.client.create(parent+"/"+PORT, value = work.port)
        self.client.create(parent+"/"+STATUS, value = work.status)
        self.client.create(parent+"/"+SERVICE_STATUS, value = work.serviceStatus)
        
        if work.brokerServer:
            self.client.create(parent+"/"+BROKER_SERVER, value=work.brokerServer)
            self.client.create(parent+"/"+QUEUES)
            for q in work.queues:
                self.client.create(parent+"/"+QUEUES+"/"+q)
        else:
            self.client.create(parent+"/"+BROKER_SERVER)
            self.client.create(parent+"/"+QUEUES)
        
        self.client.create("/"+CABBAGE+"/"+WORKS+"/"+READIES+"/"+work.hostName)
        
    def updateWorkStatus(self,work):
        parent="/"+CABBAGE+"/"+WORKS+"/"+work.hostName
        self.client.putData(parent+"/"+STATUS,  work.status)
    
    def updateWorkServiceStatus(self,work):
        parent="/"+CABBAGE+"/"+WORKS+"/"+work.hostName
        if not self.client.isExistPath(parent+"/"+SERVICE_STATUS):
            self.client.create(parent+"/"+SERVICE_STATUS, value = work.serviceStatus)
        else:
            self.client.putData(parent+"/"+SERVICE_STATUS,  work.serviceStatus)
    
        
    def saveQueue(self,q):
        parent="/"+CABBAGE+"/"+QUEUE_SERVER+"/"+QUEUES+"/"+q.queueName
        if self.client.isExistPath(parent):
            self.client.delete(parent,recursive=True)
            
        self.client.create(parent,makepath=True)
        self.client.create(parent+"/"+EXCHANGE, value = q.exchangeName)
        self.client.create(parent+"/"+ROUTING_KEY, value = q.routingKey)
        self.client.create(parent+"/"+SERVER, value = q.server)
        self.client.create(parent+"/"+WORKS)
        if q.works:
            for w in q.works:
                self.client.create(parent+"/"+WORKS+"/"+w)
    
    def saveBrokerServer(self,brokeServer):
        
        parent="/"+CABBAGE+"/"+QUEUE_SERVER+"/"+BROKER_SERVERS+"/"+brokeServer.hostName
        if self.client.isExistPath(parent):
            self.client.delete(parent,recursive=True)
            
        self.client.create(parent,makepath=True)
        self.client.create(parent+"/"+CONNECT_URI, value = brokeServer.connectUri)
        self.client.create(parent+"/"+SERVER_TYPE, value = brokeServer.serverType)
        self.client.create(parent+"/"+IP, value = brokeServer.ip)
        self.client.create(parent+"/"+PORT, value = brokeServer.port)
        self.client.create(parent+"/"+QUEUES)
        self.client.create(parent+"/"+WORKS)
        
        for q in brokeServer.queues:
            self.client.create(parent+"/"+QUEUES+"/"+q)
        
        if brokeServer.works:
            for w in q.works:
                self.client.create(parent+"/"+WORKS+"/"+w)
                
        self.client.create("/"+CABBAGE+"/"+QUEUE_SERVER+"/"+BROKER_SERVERS+"/"+READIES+"/"+brokeServer.hostName)
    
    def isExistBrokerServer(self,hostName):
        return self.client.isExistPath("/"+CABBAGE+"/"+QUEUE_SERVER+"/"+BROKER_SERVERS+"/"+hostName)
    
            
    def getQueue(self,queueName):
        parent="/"+CABBAGE+"/"+QUEUE_SERVER+"/"+QUEUES+"/"+queueName
        
        exchange = self.client.getData(parent+"/"+EXCHANGE)
        routingKey = self.client.getData(parent+"/"+ROUTING_KEY)
        serverHostName =self.client.getData(parent+"/"+SERVER)
        works = self.client.getChildren(parent+"/"+WORKS)
        
        return BrokerQueue(server=serverHostName,queueName=queueName,exchangeName=exchange,routingKey=routingKey,works=works)
    
    def isExistQueue(self,queueName):
        parent="/"+CABBAGE+"/"+QUEUE_SERVER+"/"+QUEUES+"/"+queueName
        return self.client.isExistPath(parent)
    
    def getQueues(self):
        parent="/"+CABBAGE+"/"+QUEUE_SERVER+"/"+QUEUES
        queues = self.client.getChildren(parent)
        qs = []
        for q in queues:
            qs.append(self.getQueue(q)) 
            
        return qs
    
    def getBrokerServer(self,hostName):
        parent="/"+CABBAGE+"/"+QUEUE_SERVER+"/"+BROKER_SERVERS+"/"+hostName
        connectUri = self.client.getData(parent+"/"+CONNECT_URI)
        serverType = self.client.getData(parent+"/"+SERVER_TYPE)
        ip  = self.client.getData(parent+"/"+IP)
        port = self.client.getData(parent+"/"+PORT)
        queues = self.client.getChildren(parent+"/"+QUEUES)
         
        works = self.client.getChildren(parent+"/"+WORKS)
        
        return  BrokerServer(port=port,ip=ip,serverType=serverType,connectUri=connectUri,hostName=hostName,queues=queues,works=works)
    
    def getBrokerServers(self):
        parent="/"+CABBAGE+"/"+QUEUE_SERVER+"/"+BROKER_SERVERS
        servers = self.client.getChildren(parent)
        ps = []
        for hostName in servers:
            if hostName ==READIES:
                continue
            ps.append(self.getBrokerServer(hostName))
        
        return ps
    
    def addServerBrokerQueue(self,server,brokerQueue):
        parent="/"+CABBAGE+"/"+QUEUE_SERVER+"/"+BROKER_SERVERS+"/"+server.hostName
        self.client.create(parent+"/"+QUEUES+"/"+brokerQueue.queueName)  
        if brokerQueue.works:
            for w in brokerQueue.works:
                if not self.client.isExistPath(parent+"/"+WORKS+"/"+w):
                    self.client.create(parent+"/"+WORKS+"/"+w)
    
    
    def addWorkBrokerServerBrokerQueue(self,work,brokerServer,brokerQueue):
        parent="/"+CABBAGE+"/"+WORKS+"/"+work.hostName
        
#         if not self.client.isExistPath(parent+"/"+BROKER_SERVER):
#             self.client.create(parent+"/"+BROKER_SERVER, value=brokerServer)
#             self.client.create(parent+"/"+BROKER_SERVER+"/"+QUEUES)
#         else:
        if work.brokerServer != brokerServer: #切换集群
                self.client.putData(parent+"/"+BROKER_SERVER, brokerServer)
                queues = self.client.getChildren(parent+"/"+QUEUES)
                self.client.putData(parent+"/"+QUEUES, DO_NOTHING)
                for q in queues:
                    self.client.delete(parent+"/"+QUEUES+"/"+q)
                #切换队列服务器时
                time.sleep(10)
        else:
            self.client.putData(parent+"/"+BROKER_SERVER,brokerServer)   
        
        self.client.putData(parent+"/"+QUEUES, DO_SOMETHING)
        self.client.create(parent+"/"+QUEUES+"/"+brokerQueue)        
    
    
    def removeWorkFromQueue(self,queueName,work):
        parent="/"+CABBAGE+"/"+QUEUE_SERVER+"/"+QUEUES+"/"+queueName+"/"+WORKS+"/"+work
        if  self.client.isExistPath(parent):
            self.client.delete(parent)
            
    
    def _isExist(self,path):
        return self.client.isExistPath(path)
    
    def getJobMonitor(self,jobId):
        jobPath="/"+CABBAGE+"/"+MONITOR+"/"+JOBS+"/"+jobId
        if not self._isExist(jobPath):
            return None
        
        taskJobReceived =None
        if self.client.isExistPath(jobPath+"/"+TASK_RECEIVED):
            taskJobReceived=self.client.getData(jobPath+"/"+TASK_RECEIVED)
                
        taskCount,taskSucceeded,taskFailed,taskRuntime,taskQueueTime=self._getMonitor(jobPath)
        tasks  = self.client.getChildren(jobPath+"/"+TASKS)
        tas = []
        for t in tasks:
            p=jobPath+"/"+TASKS+"/"+t
            tc,ts,tf,tr,tq = self._getMonitor(p)
            taskReceived =None
            if self.client.isExistPath(p+"/"+TASK_RECEIVED):
                taskReceived=self.client.getData(p+"/"+TASK_RECEIVED)
                
            tas.append(TaskMonitor(taskCount=tc,taskSucceeded=ts,taskFailed=tf,taskRuntime=tr,taskName=t,jobId=jobId,taskQueueTime=tq,taskReceived=taskReceived))
            
        return JobMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,taskMonitors=tas,jobId=jobId,taskQueueTime=taskQueueTime,taskReceived=taskJobReceived) 
        
    def  _getMonitor(self,path):
        taskCount = self.client.getData(path+"/"+TASK_COUNT)
        taskSucceeded= self.client.getData(path+"/"+TASK_SUCCEEDED)
        taskFailed= self.client.getData(path+"/"+TASK_FAILED)
        taskRuntime=self.client.getData(path+"/"+TASK_RUNTIME)
        taskQueueTime=None
        if self.client.isExistPath(path+"/"+TASK_QUEUE_TIME):
            taskQueueTime=self.client.getData(path+"/"+TASK_QUEUE_TIME)
        
        return  taskCount,taskSucceeded,taskFailed,taskRuntime,taskQueueTime
    
    def getWorkMonitor(self,hostName):
        workPath="/"+CABBAGE+"/"+MONITOR+"/"+WORKS+"/"+hostName
        if not self._isExist(workPath):
            return None
        taskCount,taskSucceeded,taskFailed,taskRuntime,taskQueueTime=self._getMonitor(workPath)
        
        tasks  = self.client.getChildren(workPath+"/"+TASKS)
        tas = []
        for t in tasks:
            p=workPath+"/"+TASKS+"/"+t
            tc,ts,tf,tr,tq = self._getMonitor(p)
            jp=workPath+"/"+TASKS+"/"+t+"/"+JOB_ID
            jobId=self.client.getData(jp)
            
            tas.append(TaskMonitor(taskCount=tc,taskSucceeded=ts,taskFailed=tf,taskRuntime=tr,taskName=t,jobId=jobId,taskQueueTime=tq))
        
        return WorkMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,taskMonitors=tas,hostName=hostName)

    def getWorkDateMonitors(self,hostName,date):
        p="/"+CABBAGE+"/"+MONITOR+"/"+WORKS+"/"+hostName+"/"+DATES+"/"+date
        
        if self.client.isExistPath(p):
            h=[]
            hours =self.client.getChildren(p)
            for hour in hours:
                h.append(self.getWorkHourMonitor(hostName, date, hour))
            return h
        return None
    
    def getWorkHourMonitor(self,hostName,date,hour):
        p="/"+CABBAGE+"/"+MONITOR+"/"+WORKS+"/"+hostName+"/"+DATES+"/"+date+"/"+hour
        if self.client.isExistPath(p):
            tc,ts,tf,tr,tq = self._getMonitor(p)
            return DateMonitor(taskCount=tc,taskSucceeded=ts,taskFailed=tf,taskRuntime=tr,date=date,hour=hour)
                
        return None
    
    
    def getBrokerMonitor(self,brokerServer):
        brokerPath="/"+CABBAGE+"/"+MONITOR+"/"+BROKER_SERVERS+"/"+brokerServer
        if self.client.isExistPath(brokerPath):
            taskCount,taskSucceeded,taskFailed,taskRuntime,taskQueueTime=self._getMonitor(brokerPath)
            return BrokerMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,brokerServer=brokerServer,taskQueueTime=taskQueueTime)
    
    def getBrokerDateMonitor(self,brokerServer,date):
        p="/"+CABBAGE+"/"+MONITOR+"/"+BROKER_SERVERS+"/"+brokerServer+"/"+DATES+"/"+date
        if self.client.isExistPath(p):
            tc,ts,tf,tr,tq = self._getMonitor(p)
            return DateMonitor(taskCount=tc,taskSucceeded=ts,taskFailed=tf,taskRuntime=tr,date=date,taskQueueTime=tq)

        return None
    def getJobMonitors(self):
        jobPath="/"+CABBAGE+"/"+MONITOR+"/"+JOBS
        ms = []
        jobIds = self.client.getChildren(jobPath)
        for jobId in jobIds:
            ms.append(self.getJobMonitor(jobId))
        
        return ms
    
    def getWorkMonitors(self):
        workPath="/"+CABBAGE+"/"+MONITOR+"/"+WORKS
        ws = []
        
        works = self.client.getChildren(workPath)
        for hostName in works:
            ws.append(self.getWorkMonitor(hostName))
            
        return ws
    
    def getBrokerMonitors(self):
        brokerPath="/"+CABBAGE+"/"+MONITOR+"/"+BROKER_SERVERS
        bs = [] 
        
        brokers = self.client.getChildren(brokerPath)
        
        for broker in brokers:
            bs.append(self.getBrokerMonitor(broker))
        
        return bs
    
    
    
    def _updateMonitor(self,path,obj):
        if self.client.isExistPath(path):
            self.client.putData(path+"/"+TASK_COUNT,str(obj.taskCount))
            self.client.putData(path+"/"+TASK_SUCCEEDED,str(obj.taskSucceeded))
            self.client.putData(path+"/"+TASK_FAILED,str(obj.taskFailed))
            self.client.putData(path+"/"+TASK_RUNTIME,str(obj.taskRuntime))
            
            if hasattr(obj,TASK_RECEIVED):
                self.client.putData(path+"/"+TASK_RECEIVED,str(obj.taskReceived))
                
            if hasattr(obj,TASK_QUEUE_TIME):
                self.client.putData(path+"/"+TASK_QUEUE_TIME,str(obj.taskQueueTime))
        else:
            self.client.create(path+"/"+TASK_COUNT,value=str(obj.taskCount),makepath=True)
            self.client.create(path+"/"+TASK_SUCCEEDED,value=str(obj.taskSucceeded))
            self.client.create(path+"/"+TASK_FAILED,value=str(obj.taskFailed))
            self.client.create(path+"/"+TASK_RUNTIME,value=str(obj.taskRuntime))
            
            if hasattr(obj,TASK_QUEUE_TIME):
                self.client.create(path+"/"+TASK_QUEUE_TIME,value=str(obj.taskQueueTime))
            
            if hasattr(obj,TASK_RECEIVED):
                self.client.create(path+"/"+TASK_RECEIVED,value=str(obj.taskReceived))
    
    def saveMonitor(self,monitor):
        parent="/"+CABBAGE+"/"+MONITOR
        for jobMonitor in monitor.jobMonitors:
            jobPath=parent+"/"+JOBS+"/"+jobMonitor.jobId
            self._updateMonitor(jobPath,jobMonitor)
            for task in jobMonitor.taskMonitors:
                self._updateMonitor(jobPath+"/"+TASKS+"/"+task.taskName,task)
                
        for workMonitor in monitor.workMonitors:
            workPath=parent+"/"+WORKS+"/"+workMonitor.hostName
            self._updateMonitor(workPath, workMonitor)
            for task in workMonitor.taskMonitors:
                self._updateMonitor(workPath+"/"+TASKS+"/"+task.taskName, task)
                jp=workPath+"/"+TASKS+"/"+task.taskName+"/"+JOB_ID
                if self.client.isExistPath(jp):
                    self.client.putData(jp,task.jobId)
                else:
                    self.client.create(jp,value=task.jobId)
                
            for dateMonitor in workMonitor.dateMonitors:
                datePath = parent+"/"+WORKS+"/"+workMonitor.hostName+"/"+DATES+"/"+dateMonitor.date+"/"+dateMonitor.hour
                self._updateMonitor(datePath, dateMonitor)
            
        for brokerMonitor in monitor.brokerMonitors:
            brokerPath=parent+"/"+BROKER_SERVERS+"/"+brokerMonitor.brokerServer
            
            self._updateMonitor(brokerPath, brokerMonitor)
            
            for dateMonitor in brokerMonitor.dateMonitors:
                datePath = parent+"/"+BROKER_SERVERS+"/"+brokerMonitor.brokerServer+"/"+DATES+"/"+dateMonitor.date
                self._updateMonitor(datePath, dateMonitor)
        
            
    def saveConfig(self,config):
        parent = "/"+CABBAGE+"/"+CONFIG+"/"+config.key
        if not self.client.isExistPath(parent):
            self.client.create(parent, config.value)
            self.client.create(parent+"/"+DESC,value=config.desc)
        else:
            self.client.putData(parent, config.value)
            self.client.putData(parent+"/"+DESC,config.desc)
        
    def getConfig(self,key):
        parent = "/"+CABBAGE+"/"+CONFIG+"/"+key
        if self.client.isExistPath(parent):
            value = self.client.getData(parent)
            desc=None
            
            if  self.client.isExistPath(parent+"/"+DESC):
                desc  = self.client.getData(parent+"/"+DESC)
                
            return Config(key,value,desc=desc)
            
        return None
    
    
    def getConfigs(self):
        parent = "/"+CABBAGE+"/"+CONFIG
        keys = self.client.getChildren(parent)
        configs = []
        for key in keys:
            configs.append(self.getConfig(key))
        
        return configs
    
    def saveTaskId(self,jobId,taskName,taskId):
        parent="/"+CABBAGE+"/"+JOBS+"/"+RESULTS
        self.client.create(parent+"/"+taskId,value=str(jobId+"@"+taskName))
        
    def getTaskId(self,taskId):
        parent="/"+CABBAGE+"/"+JOBS+"/"+RESULTS
        if  self.client.isExistPath(parent+"/"+taskId):
            return self.client.getData(parent+"/"+taskId)
        
    def deleteTaskId(self,taskId):
        parent="/"+CABBAGE+"/"+JOBS+"/"+RESULTS+"/"+taskId
        if  self.client.isExistPath(parent):
            self.client.delete(parent)
        
    def getTaskIdsByJobId(self,jobId):
        parent="/"+CABBAGE+"/"+JOBS+"/"+RESULTS+"/"+jobId
        if  self.client.isExistPath(parent):
            tasks = {}
            taskNames = self.client.getChildren(parent)
            for taskName in taskNames:
                tasks[taskName] =self.client.getChildren(parent+"/"+taskName) 
                
            return tasks
        
    def getRunJobs(self):
        parent="/"+CABBAGE+"/"+JOBS+"/"+RESULTS
        if self.client.isExistPath(parent):
            return self.client.getChildren(parent)
        return []
    
    
    def addJobWork(self,jobId,work):
        parent="/"+CABBAGE+"/"+JOBS+"/"+jobId
        self.client.create(parent+"/"+WORKS+"/"+LIST+"/"+work.hostName,value=work.port,makepath=True)

    def addQueueWork(self,brokerQueue,work):
        parent="/"+CABBAGE+"/"+QUEUE_SERVER+"/"+QUEUES+"/"+brokerQueue.queueName
        self.client.create(parent+"/"+WORKS+"/"+work.hostName)
        
        parent="/"+CABBAGE+"/"+QUEUE_SERVER+"/"+BROKER_SERVERS+"/"+brokerQueue.server+"/"+WORKS+"/"+work.hostName
        if not self.client.isExistPath(parent):
            self.client.create(parent)

    def addWorkQueue(self,brokerQueue,work):
        parent="/"+CABBAGE+"/"+WORKS+"/"+work.hostName
        
        #fixbug 初始机器没有集群
        if work.brokerServer == "":
            self.client.putData(parent+"/"+BROKER_SERVER,brokerQueue.server)  
        
        self.client.create(parent+"/"+QUEUES+"/"+brokerQueue.queueName)
    
    
#     def addUser(self,user):
#         parent="/"+CABBAGE+"/"+USERS+"/"+user.userName
#         if not self.client.isExistPath(parent):
#             self.client.create(parent)
#             self.client.create(parent+"/"+USER_PWD,value=user.userPwd)
#             self.client.create(parent+"/"+IS_ADMIN,value=user.isAdmin)
        
        
        
    
    
    
    