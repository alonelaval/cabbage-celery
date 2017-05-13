# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''
from __future__ import absolute_import
from cabbage.cabbage_celery.main import CabbageMain
from zope.interface.declarations import implementer
from test_nfs_task import TestNfsTask
import time
class TestNfsMain(CabbageMain):
    def run(self,*args,**kwargs):
#         print kwargs
#         print self.getApp()
        print self.job.jobId
#         print self.job.brokerServer
        self.apply_async(TestNfsTask,kwargs={"no":args[0]})
        
#         print self.getApp().tasks
#         TestHdfsTask.bind(self.getApp())
#         task = TestHdfsTask()
#         result = task.apply_async((1,2,args[0]),expires=5)
# #         delay(1,2,expires=5)
#         self.addResult(result)
#         print "main:"+str(result)
#         while(1):
#             if result.ready():
#                 print "result:"+str(result.result)
#                 break
#             if result.failed():
#                 print "result:"+str(result.result)
#                 break
#             print result.status
#             time.sleep(2)

