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


class TestHdfsTask(CabbageTask):
    
    def doRun(self,aaa=1,bbb=2,no=None):
        
         if random.randint(0,10) % 2 == 0:
             print self.jobId,no
             self.addResult(getNow())
             return "fuck"
                 
         return "hello world!"
        
        
#     def run(self,aaa=1,bbb=2,no=None):
#         print self.
#         print "NO:%s"%no
#         print aaa,bbb
#         return aaa  * bbb
#     
# @implementer(CabbageMain)
# class TestMain():
#     def run(self,aaa=1,bbb=2):
#         task = TestTask()
#         result = task.delay(1,2)
#         print "main:"+str(result)
#         print "result:"+str(result.result)
