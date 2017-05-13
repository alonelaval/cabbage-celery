# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''

# from celery import Task
from cabbage.cabbage_celery.main import CabbageMain
from cabbage.cabbage_celery.task import CabbageTask
from zope.interface.declarations import implementer

# app = Celery('cabbage',backend="rpc://",broker='amqp://172.16.4.134')

def sayHello():
    print "hello world!"

class TestUbuntuTask(CabbageTask):
    def doRun(self,aaa=1,bbb=2,no=None):
        print "NO:%s"%no
#         print "加料"
        print aaa,bbb
        return aaa  * bbb
    
# @implementer(CabbageMain)
# class TestMain():
#     def run(self,aaa=1,bbb=2):
#         task = TestTask()
#         result = task.delay(1,2)
#         print "main:"+str(result)
#         print "result:"+str(result.result)
