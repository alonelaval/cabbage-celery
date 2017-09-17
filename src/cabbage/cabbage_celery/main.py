# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''

from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.constants import JOB_ID
# from cabbage.data.store_holder import StoreHolder
from zope.interface.declarations import implementer
from zope.interface.interface import Interface
import uuid
# from cabbage.data.store_holder import StoreHolder
class Main(Interface):
    pass

@implementer(Main)
class CabbageMain(object):
    def __init__(self):
        self.results=[]
#         self.app=None
        self.job=None
#         self.store= StoreHolder.getRetryStore()
        
    def addResult(self,taskName,taskId):
#         print taskId
#         self.store.saveTaskId( self.job.jobId,taskName,taskId)
#         self.results.append(result)
        pass
    def _addTaskTrack(self,taskName,taskId):
#         with storeFactory.store() as store:
#             store.saveTaskId(self.job.jobId,taskName,taskId)
            pass
        
    def getApp(self):
        return CabbageHolder.getServerCabbage(self.job.brokerServer).getApp()
        
    def getResults(self):
        return self.results 
    '''
        本地调用方法接口
    '''
    def apply_async(self,cls,args=None,kwargs=None,**options):
        cls.bind(self.getApp())
       
        obj = cls()
        if kwargs:
            kwargs[JOB_ID]= self.job.jobId
        else:
            kwargs= {JOB_ID: self.job.jobId}
        from cabbage.common.cabbage_celery.util import isCabbageTask
        taskName = None
        if isCabbageTask(cls):
            taskName = cls.__module__  +"."+ cls.__name__
#         print taskName 
        self.getApp().register_task(obj)
        result =obj.apply_async(args=args,task_id=self.getTaskId(taskName),kwargs=kwargs,**options)
        return result
#         self._addTaskTrack(taskName,result.id)
        
    def getTaskId(self,taskName):
        return str(uuid.uuid4()) +"@"+ self.job.jobId+"@"+taskName 
    
    def send_task(self,taskName,args=None,kwargs=None,**options):
        if kwargs:
            kwargs[JOB_ID] = self.job.jobId
        else:
            kwargs= {JOB_ID: self.job.jobId}
            
        result =self.getApp().send_task(taskName,task_id=self.getTaskId(taskName), args=args,kwargs=kwargs,**options)
#         self._addTaskTrack(taskName,result.id)
        return result
                
    def run(self,*args,**kwargs):
        print args
        print "fuck"
        pass
