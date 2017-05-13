# -*- encoding: utf-8 -*-
'''
Created on 2016年10月9日

@author: huawei
'''
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.constants import OFF_LINE, ON_LINE, REMOVE
from cabbage.event.server_jobs_event import WorkStatusEvent
from cabbage.machine.work_contorl import WorkContorl
from zope.interface.declarations import implementer
import zope.event

@implementer(WorkContorl)
class CeleryWorkContorl(object):
    def __init__(self,work):
        self.work=work
        
    def startService(self):
        zope.event.notify(WorkStatusEvent(self.work.hostName,ON_LINE))

    def stopService(self):
        if (CabbageHolder.getServerCabbage(self.work.brokerServer).workIsAlive(self.work.hostName)):
            CabbageHolder.getServerCabbage(self.work.brokerServer).stop(self.work.hostName)
            
        zope.event.notify(WorkStatusEvent(self.work.hostName,OFF_LINE))
            
    def serviceIsAlive(self):
        if len(CabbageHolder.getServerCabbage(self.work.brokerServer).ping(self.work.hostName)) >0:
            return True
            
        return False
    
    def stop(self):
        if (CabbageHolder.getServerCabbage(self.work.brokerServer).workIsAlive(self.work.hostName)):
            CabbageHolder.getServerCabbage(self.work.brokerServer).stop(self.work.hostName)
        zope.event.notify(WorkStatusEvent(self.work.hostName,REMOVE))
