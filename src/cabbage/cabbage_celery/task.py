# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''
# from zope.interface.interface import Interface
from celery import Task
from cabbage.constants import JOB_ID
from cabbage.job.job_results import jobResults
# from cabbage.config import ConfigHolder

class CabbageTask(Task):
    abstract = True
    '''
        定义远程方法接口
    '''
    def run(self,*args,**kwargs):
        if kwargs and JOB_ID in kwargs:
            self.jobId = kwargs.pop(JOB_ID,None)
        
        return self.doRun(*args,**kwargs)
        
    def addResult(self,data):
        if data and data != "":
            jobResults.addResult(self.jobId, data)
#             print jobResults
#             print ConfigHolder.getConfig()
#             print ConfigHolder.getConfig().getProperty(BASE, JOB_EXECUTOR_COUNT)
        
        
    def doRun(self,*args,**kwargs):
        print "CabbageTask hello world" 
    

