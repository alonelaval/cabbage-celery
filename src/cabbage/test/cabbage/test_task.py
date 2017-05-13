# -*- encoding: utf-8 -*-
'''
Created on 2016年6月24日

@author: hua
'''
from cabbage.cabbage_celery.task import CabbageTask
from zope.interface.declarations import implementer, directlyProvides, \
    classProvides, providedBy, implementedBy
import unittest
class MyTask():
    def run(self,aaa=1,bbb=2):
        print aaa,bbb

class TestTask(unittest.TestCase):
    def test_impl(self):
        myTask = MyTask()
#         print CabbageTask.implementedBy(MyTask)
#         print directlyProvides(myTask,Task)
        print type(MyTask)
        print list(providedBy(myTask))[0]
        print list(implementedBy(MyTask))
        myTask.run()
        pass
    
if __name__=="__main__":
    unittest.main()
