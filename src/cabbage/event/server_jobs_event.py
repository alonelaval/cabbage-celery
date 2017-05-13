# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''


import zope.event.classhandler

class JobUpdateEvent(object):
    def __init__(self,jobId,status=None):
        self.jobId = jobId
        self.status = status
    def __repr__(self):
        return self.__class__.__name__

class JobRemoveEvent(object):
    def __init__(self,jobId):
        self.jobId = jobId
    def __repr__(self):
        return self.__class__.__name__

class JobRunEvent(object):
    def __init__(self,jobId,params=None,ignoreNotPerWork=True):
        self.jobId = jobId
        self.params=params
        self.ignoreNotPerWork=ignoreNotPerWork
    def __repr__(self):
        return self.__class__.__name__
    
class JobAuditEvent(object):
    def __init__(self,jobId,status):
        self.jobId = jobId
        self.status =status
    def __repr__(self):
        return self.__class__.__name__
    
class AddBrokerServerEvent(object):
    def __init__(self,brokerServer):
        self.brokerServer =brokerServer
    def __repr__(self):
        return self.__class__.__name__
    
class MonitorBrokerServerEvent(object):
    def  __init__(self,brokerServer):
        self.brokerServer = brokerServer

class WorkStatusEvent(object):
    def __init__(self,hostName,status):
        self.hostName =hostName
        self.status = status
class WorkServiceStatusEvent(object):
    def __init__(self,hostName,status):
        self.hostName =hostName
        self.status = status
    
    
def registerServerEvent():
    from cabbage.event.handler.server_event_handler import jobUpdateHandler,jobRunHandler,jobRemoveHandler
    from cabbage.event.handler.server_event_handler import jobAuditStatusHandler,addBroberServerHandler, workStatusHandler,monitorBroberServerHandler,workServiceStatusHandler
    #注册
    zope.event.classhandler.handler(JobUpdateEvent, jobUpdateHandler)
    zope.event.classhandler.handler(JobRemoveEvent, jobRemoveHandler)
    zope.event.classhandler.handler(JobRunEvent,jobRunHandler)
    zope.event.classhandler.handler(JobAuditEvent,jobAuditStatusHandler)
    zope.event.classhandler.handler(AddBrokerServerEvent,addBroberServerHandler)
    zope.event.classhandler.handler(MonitorBrokerServerEvent,monitorBroberServerHandler)
    zope.event.classhandler.handler(WorkStatusEvent,workStatusHandler)
    zope.event.classhandler.handler(WorkServiceStatusEvent,workServiceStatusHandler)
    
    
