# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''

from cabbage.cabbage_celery.task import CabbageTask

from celery import Task

def sayHello():
    print "hello world!"

class TestMacTask(CabbageTask):
    def doRun(self,aaa=1,bbb=2,no=None):
        print "NO:%s"%no
        print "加料"
        print aaa,bbb
        return aaa  * bbb
    
class DebugTask(Task):
#     def __init__(self):
#         self.name = self.__name__
#         print self.__class__
        
    def __call__(self, *args, **kwargs):
        print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)
    
    def run(self):
        print "hello world"