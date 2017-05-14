# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''

from cabbage.cabbage_celery.main import CabbageMain
from cabbage.cabbage_celery.task import CabbageTask
from zope.interface.declarations import implementer

def sayHello():
    print "hello world!"

class TestUbuntuTask(CabbageTask):
    def doRun(self,aaa=1,bbb=2,no=None):
        print "NO:%s"%no
#         print "加料"
        print aaa,bbb
        print sayHello()
        return aaa  * bbb
    
