# -*- encoding: utf-8 -*-
'''
Created on 2016年8月9日

@author: hua
'''
from cabbage.process.cabbage_job_excutor import \
    CabbageJobExecutorHolder
from unittest.case import TestCase
import unittest
class SayHelloEvent():
    def __repr__(self):
        return self.__class__.__name__

def sayHelloHandler(event):
    print "sayHello"
    print  "sayHello"



class TestServer(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
#         zope.event.classhandler.handler(SayHelloEvent,sayHelloHandler)
    def test_executor(self):
        excutor = CabbageJobExecutorHolder.getCabbageJobExecutor()
        for i in range(100):
            excutor.add(SayHelloEvent())
    

if __name__=="__main__":
    unittest.main()