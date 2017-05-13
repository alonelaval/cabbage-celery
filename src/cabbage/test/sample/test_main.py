# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''

from __future__ import absolute_import
from cabbage.cabbage_celery.main import CabbageMain
from cabbage.test.sample.test_task import TestTask
from zope.interface.declarations import implementer

@implementer(CabbageMain)
class TestMain():
    def run(self,aaa=1,bbb=2):
#         result = TestTask.run.delay(1,2)

        pass
