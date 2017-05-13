# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''

from cabbage.cabbage_celery.task import CabbageTask
from zope.interface.declarations import implementer

def sayHello():
    print "hello world!"
    

@implementer(CabbageTask)
class TestTask():
    def run(self,aaa=1,bbb=2):
        sayHello()
        print aaa,bbb
        return aaa  * bbb