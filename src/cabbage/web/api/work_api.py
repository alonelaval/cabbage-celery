# -*- encoding: utf-8 -*-
'''
Created on 2016年8月4日

@author: hua
'''
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.constants import REMOVE, ON_LINE, OFF_LINE
from cabbage.machine.celery_work_contorl import CeleryWorkContorl
from cabbage.web.api.util import excute
class WorkApi(object):
    @excute
    def getWorks(self,store):
        return store.getWorks()
    
    @excute
    def addWorkQueue(self,store,brokerQueue,work):
        store.addWorkQueue(brokerQueue,work)
    
    def stopWorkService(self,work):
        if (CabbageHolder.getServerCabbage(self.work.brokerServer).workIsAlive(self.work.hostName)):
            CabbageHolder.getServerCabbage(self.work.brokerServer).stop(self.work.hostName)
    @excute
    def getWork(self,store,hostName):
        return store.getWork(hostName)
    def workChangeStatus(self,work,status):
        if status == REMOVE:
            CeleryWorkContorl(work).stop()
        if status == ON_LINE:
            CeleryWorkContorl(work).startService()
        if status == OFF_LINE:
            CeleryWorkContorl(work).stopService()