# -*- encoding: utf-8 -*-
'''
Created on 2016年6月8日

@author: hua
'''
from zope.interface.interface import Interface


class Store(Interface):
    def getJobs(self):
        pass
    def getJobIds(self):
        pass
    def getJob(self,jobId):
        pass
    def saveJob(self,job):
        pass
    def updateJobStatus(self,jobId,jobStatus):
        pass
    def updateAuditStatus(self,jobId,auditStatus):
        pass
    def updateJobWorkReady(self,jobId,work):
        pass
    def removeJobWorkReady(self,jobId,work):
        pass
    def getJobWorksReadyDone(self,jobId):
        pass
    def getFiles(self):
        pass
    def saveFile(self,f):
        pass
    def getFile(self,fileName):
        pass
    def getAuths(self):
        pass
    def saveAuth(self,auth):
        pass
    def getAuth(self,jobId):
        pass
    def getUsers(self):
        pass
    def saveUser(self,user):
        pass
    def getUser(self,userName):
        pass
    def getWork(self,hostName):
        pass
    def getWorks(self):
        pass
    def saveWork(self,work):
        pass
    def updateWorkStatus(self,work):
        pass
    def updateWorkServiceStatus(self,work):
        pass
    def saveQueue(self,q):
        pass
    def saveBrokerServer(self,brokeServer):
        pass
    def getQueue(self,queueName):
        pass
    def isExistQueue(self,queueName):
        pass
    def isExistBrokerServer(self,hostName):
        pass
    def getQueues(self):
        pass
    def getBrokerServer(self,hostName):
        pass
    def getBrokerServers(self):
        pass
    def addServerBrokerQueue(self,server,borkerQueue):
        pass
    def removeWorkFromQueue(self,queue,work):
        pass
    
    def addWorkBrokerServerBrokerQueue(self,work,brokerServer,brokerQueue):
        pass
    def isExistWork(self,work):
        pass
    
    def getJobMonitor(self,jobId):
        pass
    
    def getWorkMonitor(self,hostName):
        pass
    
    def getBrokerMonitor(self,brokerServer):
        pass
    def getBrokerDateMonitor(self,brokerServer,date):
        pass
    def getJobMonitors(self):
        pass
    
    def getWorkMonitors(self):
        pass
    
    def getWorkDateMonitors(self,hostName,date):
        pass
    def getWorkHourMonitor(self,hostName,date,hour):
        pass
    
    def getBrokerMonitors(self):
        pass
    
    def saveMonitor(self,monitor):
        pass
    def saveConfig(self,config):
        pass
    def getConfig(self,key):
        pass
    def getConfigs(self):
        pass
    
    def saveTaskId(self,jobId,taskName,taskId):
        pass
    def getTaskId(self,taskId):
        pass
    
    def deleteTaskId(self,taskId):
        pass
    def getTaskIdsByJobId(self,jobId):
        pass
    def getRunJobs(self):
        pass
    def close(self):
        pass
    
    def addJobWork(self,jobId,work):
        pass
    
    def addQueueWork(self,brokerQueue,work):
        pass
    
    def addWorkQueue(self,brokerQueue,work):
        pass
    
    def addUser(self,user):
        pass