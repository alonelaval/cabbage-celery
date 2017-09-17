# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''
from __future__ import absolute_import
from cabbage.cabbage_celery.main import CabbageMain
from zope.interface.declarations import implementer
from test_mac_task import TestMacTask
import time
class TestMac(CabbageMain):
    def run(self,*args,**kwargs):
#         print args
#         print kwargs
#         print self.getApp()
#         print self.job
#         print self.job.brokerServer
#         
#         print self.getApp().tasks
#         TestMacTask.bind(self.getApp())
#         task = TestMacTask()
#         result = task.apply_async((1,2,args[0]),expires=5)
#         conf = self.getApp().conf
#         for key,value in conf.items():
#             print "key : %s  value: %s " %(key , value)
        
        for k,v in self.getApp().conf.items():
            print "key : %s  value: %s " %(k , v)
            
        print "CELERY_ROUTES:[%s]" % self.getApp().conf["CELERY_ROUTES"]
#         self.send_task('test_mac_task.TestMacTask',args=(1,2,args[0]),expires=5) 
        self.apply_async(TestMacTask,(1,2,args[0]),expires=5)
#         self.send_task(test_mac_task.TestMacTask',, args, kwargs)

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

