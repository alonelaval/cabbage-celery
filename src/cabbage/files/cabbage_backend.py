# -*- encoding: utf-8 -*-
'''
Created on 2016年10月11日

@author: huawei
'''
from zope.interface.declarations import implementer
from zope.interface.interface import Interface


class ICabbageBackend(Interface):
   
    def save(self):
        pass
    

@implementer(ICabbageBackend)
class AbstractCabbageFileSystemBackend(object):
    def __init__(self,jobId):
        self.jobId = jobId


    
