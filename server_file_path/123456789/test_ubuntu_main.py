# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''
from __future__ import absolute_import
from cabbage.cabbage_celery.main import CabbageMain
from zope.interface.declarations import implementer
from test_ubuntu_task import TestUbuntuTask
import time
class TestUbuntuMain(CabbageMain):
    def run(self,*args,**kwargs):
#         print args
#         print kwargs
        print self.getApp()
        print self.job
        print self.job.brokerServer
        print self.getApp().tasks
        print "CELERY_ROUTES:[%s]" % self.getApp().conf["CELERY_ROUTES"] 
#         TestUbuntuTask.bind(self.getApp())
#         task = TestUbuntuTask()
#         result = task.apply_async((1,2,args[0]),expires=5)
        self.apply_async(TestUbuntuTask,(1,2,args[0]),expires=5)
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

