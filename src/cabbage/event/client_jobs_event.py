# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''


import zope.event.classhandler

class JobAuditPassEvent(object):
    def __init__(self,jobId):
        self.jobId = jobId
    def __repr__(self):
        return self.__class__.__name__

class JobStatusChangeEvent(object):
    def __init__(self,jobId):
        self.jobId = jobId
    def __repr__(self):
        return self.__class__.__name__
    
class JobNeedLoadEvent(object):
    def __init__(self,jobId):
        self.jobId = jobId
        
class WorkBrokerQueueChangeEvent(object):
    def __init__(self,brokerQueues,isEvent=False):
        self.brokerQueues = brokerQueues
        self.isEvent = isEvent
    def __repr__(self):
        return self.__class__.__name__
    
class WorkBrokerServerChangeEvent(object):
    def __init__(self,brokerServer,isEvent=False):
        self.brokerServer = brokerServer
        self.isEvent = isEvent
    def __repr__(self):
        return self.__class__.__name__
    
class ClientWorkStatusEvent(object):
    def __init__(self,status):
        self.status= status

def registerClientEvent():
    #注册
    from cabbage.event.handler.client_job_audit_pass_handler import jobAuditPassHandler
    from cabbage.event.handler.client_job_status_change_handler import jobStatusChangeHandler
    from cabbage.event.handler.client_job_need_load_handler import jobNeedLoadHandler
    from cabbage.event.handler.client_work_broker_queue_change_handler import workBrokerQueueChangeHandler
    from cabbage.event.handler.client_work_status_change_handler import clentWorkStatusChangeHandler
    
    zope.event.classhandler.handler(ClientWorkStatusEvent,clentWorkStatusChangeHandler)
    zope.event.classhandler.handler(JobAuditPassEvent, jobAuditPassHandler)
    zope.event.classhandler.handler(JobStatusChangeEvent, jobStatusChangeHandler)
    zope.event.classhandler.handler(JobNeedLoadEvent,jobNeedLoadHandler)
    zope.event.classhandler.handler(WorkBrokerQueueChangeEvent,workBrokerQueueChangeHandler)
    
    
    