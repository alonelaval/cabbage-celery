# -*- encoding: utf-8 -*-
'''
Created on 2016年6月24日

@author: hua
'''
from cabbage.cabbage_celery.main import CabbageMain
from cabbage.cabbage_celery.task import CabbageTask
import inspect

def isCabbageTask(cls):
    if inspect.isclass(cls): 
        return issubclass(cls,CabbageTask) and cls != CabbageTask
    return False

def isCabbageMain(cls):
    if inspect.isclass(cls):
        return issubclass(cls,CabbageMain) and cls != CabbageMain
    return False
