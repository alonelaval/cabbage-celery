# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''

# from celery import Task
from cabbage.cabbage_celery.task import CabbageTask
from zope.interface.declarations import implementer
import random


def sayHello():
    print "hello world!"

class TestFailTask(CabbageTask):
    def doRun(self,aaa=1,bbb=2,no=None):
        print "NO:%s"%no
        print aaa,bbb
        if random.randint(0,99) % 2 == 0:
            raise Exception("test fail!!!!!!!")
    
