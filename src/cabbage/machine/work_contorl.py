# -*- encoding: utf-8 -*-
'''
Created on 2016年10月9日

@author: huawei
'''
from zope.interface.interface import Interface
class WorkContorl(Interface):
    def startService(self):
        pass
    def stopService(self):
        pass
    def serviceIsAlive(self):
        pass
#     def offLine(self):
#         pass
#     def onLine(self):
#         pass
    def stop(self):
        pass




