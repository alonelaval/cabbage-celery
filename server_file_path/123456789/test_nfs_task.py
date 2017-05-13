# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''

# from celery import Task
from cabbage.cabbage_celery.main import CabbageMain
from cabbage.cabbage_celery.task import CabbageTask
from zope.interface.declarations import implementer
import random
from cabbage.utils.date_util import getNowDateStr, getNow

# app = Celery('cabbage',backend="rpc://",broker='amqp://172.16.4.134')


class TestNfsTask(CabbageTask):
    
    def doRun(self,aaa=1,bbb=2,no=None):
        
         self.addResult(getNow())
         if random.randint(0,10) % 2 == 0:
             print "jobId:%s\tNo:%s" % (self.jobId,no)
             return "FUCK"
         
         return "hello world!"
        
        
