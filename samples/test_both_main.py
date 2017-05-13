# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''
from __future__ import absolute_import
from cabbage.cabbage_celery.main import CabbageMain
from zope.interface.declarations import implementer
from test_both_task import TestBothTask
import time
class TestBothMain(CabbageMain):
    def run(self,*args,**kwargs):
        print args
        print kwargs
        print self.getApp()
        print self.job
        print self.job.brokerServer
        
        print self.getApp().tasks
#         TestBothTask.bind(self.getApp())
#         task = TestBothTask()
#         result = task.apply_async((1,2,args[0]),expires=5)
        
        self.apply_async(TestBothTask,(1,2,args[0]),expires=5)
#         delay(1,2,expires=5)

#         while(1):
#             if result.ready():
#                 print "result:"+str(result.result)
#                 break
#             if result.failed():
#                 print "result:"+str(result.result)
#                 break
#             print result.status
#             time.sleep(2)

