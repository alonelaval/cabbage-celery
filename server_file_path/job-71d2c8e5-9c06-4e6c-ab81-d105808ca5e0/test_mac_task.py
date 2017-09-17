# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''

from cabbage.cabbage_celery.task import CabbageTask


def sayHello():
    print "hello world!"

class TestMacTask(CabbageTask):
    def doRun(self,aaa=1,bbb=2,no=None):
        print "NO:%s"%no
        print "加料"
        print aaa,bbb
        return aaa  * bbb
