# -*- encoding: utf-8 -*-
'''
Created on 2016年6月8日

@author: huawei
'''
from cabbage.constants import JOB_AUTH_WAIT, JOB_NEW
from cabbage.utils.host_name import LOCAL_IP, HOST_NAME
import time
import uuid

class BaseEntity(object):
    def asDict(self):
        return {key: getattr(self, key) for key in self.__dict__.keys()}
    
class Job(BaseEntity):
    def __init__(self,jobId=None,jobName=None,filePath=None,auditStatus=JOB_AUTH_WAIT,
                 fileType=None,fileName=None,status=JOB_NEW,attachFiles=None,brokerServer=None,brokerQueue=None,
                 works=None,runStrategy=None,strategyValue=None,tasks=None,resultBackend=None):
        self.jobId=jobId if jobId is not None else "job-%s" % uuid.uuid4()
        self.jobName=jobName
        self.filePath=filePath
        self.fileName =fileName
        self.fileType=fileType
        self.status = status
        self.auditStatus=auditStatus
        self.attachFiles=attachFiles
        self.works=works
        self.brokerServer=brokerServer
        self.brokerQueue = brokerQueue
        self.runStrategy=runStrategy
        self.strategyValue=strategyValue
        self.tasks = tasks if tasks else []
        self.resultBackend = resultBackend
        
class Work(BaseEntity):
    def __init__(self,ip=LOCAL_IP,port=None,status=None,hostName=HOST_NAME,brokerServer=None,queues=None,queuesData=None,serviceStatus=None):
        self.ip=ip
        self.port=port
        self.status=status
        self.hostName=hostName
        self.brokerServer=brokerServer
        self.queues=queues if queues else []
        self.queuesData=queuesData
        self.serviceStatus=serviceStatus
        
    def test(self):
        pass

class Task(BaseEntity):
    def __init__(self,taskNumber=None,taskName=None,status=None,taskId=None):
        self.taskNumber=taskNumber
        self.taskName=taskName
        self.status=status
        self.taskId = taskId
        
class File(BaseEntity):
    def __init__(self,fileName=None,jobId=None,jobName=None,filePath=None,
                 fileType=None):
        self.jobId=jobId
        self.jobName=jobName
        self.filePath=filePath
        self.fileName=fileName
        self.fileType=fileType
        
class Auth(BaseEntity):
    def __init__(self,jobId=None,auditUser=None,auditStauts=None,auditTime=str(time.time())):
        self.jobId=jobId
        self.auditUser=auditUser
        self.auditTime = auditTime
        self.auditStauts = auditStauts
    
class User(BaseEntity):
    def __init__(self,userName=None,userPwd=None,isAdmin=False):
        self.userName=userName
        self.userPwd = userPwd
        self.isAdmin=isAdmin
        

class BrokerServer(BaseEntity):
    def __init__(self,port=None,ip=None,serverType=None,connectUri=None,hostName=None,queues=None,works=None):
        self.port=port
        self.ip=ip
        self.serverType=serverType
        self.connectUri=connectUri
        self.queues = queues if queues else []
        self.hostName=hostName
        self.works = works if works else []
        
class BrokerQueue(BaseEntity):
    def __init__(self,server=None,queueName=None,exchangeName=None,routingKey=None,works=None):
        self.server=server
        self.queueName=queueName
        self.exchangeName=exchangeName
        self.routingKey=routingKey
        self.works = works if works else []


class BaseMonitor(BaseEntity):
    def __init__(self,taskCount=None,taskSucceeded=None,taskFailed=None,taskRuntime=None,taskQueueTime=None):
        self.taskCount=taskCount
        self.taskSucceeded=taskSucceeded
        self.taskFailed=taskFailed
        self.taskRuntime =taskRuntime
        self.taskQueueTime = taskQueueTime
        
class TaskMonitor(BaseMonitor):
    def __init__(self,taskCount=None,taskSucceeded=None,taskFailed=None,taskRuntime=None,taskName=None,jobId=None,taskQueueTime=None,taskReceived=None):
        self.jobId=jobId
        self.taskName=taskName
        self.taskReceived=taskReceived
        super(TaskMonitor,self).__init__(taskCount,taskSucceeded,taskFailed,taskRuntime,taskQueueTime)  
        

class JobMonitor(BaseMonitor):
    def __init__(self,taskCount=None,taskSucceeded=None,taskFailed=None,taskRuntime=None,taskMonitors=None,jobId=None,taskQueueTime=None,taskReceived=None):
        self.taskMonitors=taskMonitors  if taskMonitors else []
        self.jobId=jobId
        self.taskReceived=taskReceived
        super(JobMonitor,self).__init__(taskCount,taskSucceeded,taskFailed,taskRuntime,taskQueueTime)  
        
class DateMonitor(BaseMonitor):
    def __init__(self,taskCount=None,taskSucceeded=None,taskFailed=None,taskRuntime=None,hour=None,date=None,taskQueueTime=None):
        self.hour=hour
        self.date=date
        super(DateMonitor,self).__init__(taskCount,taskSucceeded,taskFailed,taskRuntime,taskQueueTime)
        
class WorkMonitor(BaseMonitor):
    def __init__(self,taskCount=None,taskSucceeded=None,taskFailed=None,taskRuntime=None,taskMonitors=None,dateMonitors=None,hostName=None):
        self.taskMonitors=taskMonitors  if taskMonitors else []
        self.dateMonitors=dateMonitors  if dateMonitors else []
        self.hostName=hostName
        super(WorkMonitor,self).__init__(taskCount,taskSucceeded,taskFailed,taskRuntime)
        
class BrokerMonitor(BaseMonitor):
    def __init__(self,taskCount=None,taskSucceeded=None,taskFailed=None,taskRuntime=None,brokerServer=None,taskQueueTime=None,dateMonitors=None):
        self.brokerServer=brokerServer
        self.dateMonitors=dateMonitors  if dateMonitors else []
        super(BrokerMonitor,self).__init__(taskCount,taskSucceeded,taskFailed,taskRuntime,taskQueueTime)
        
        
class Monitor(BaseEntity):
    def __init__(self,jobMonitors=None,workMonitors=None,brokerMonitors=None):
        self.jobMonitors =jobMonitors
        self.workMonitors=workMonitors
        self.brokerMonitors=brokerMonitors

class Config(BaseEntity):
    def __init__(self,key,value,desc=None):
        self.key =key
        self.value=value
        self.desc =desc
        
        
        
        
