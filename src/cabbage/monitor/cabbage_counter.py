# -*- encoding: utf-8 -*-
'''
Created on 2016年9月12日

@author: huawei
'''
from cabbage.common.log.logger import Logger
from cabbage.constants import TASK_RUNTIME, TASK_COUNT, \
    TASK_QUEUE_TIME
import threading
log = Logger.getLogger(__name__)
class CabbageCounter(object):
    def __init__(self):
        self.lock =threading.Lock()
        self.taskFail={}
        self.taskSent={}
        self.taskReceived={}
        self.taskSucceeded={}
    
    def updateTaksFail(self,taskName,hostName):
        try:
            self.lock.acquire()
            if taskName in self.taskFail:
                if hostName in self.taskFail[taskName]:
                    self.taskFail[taskName][hostName]=self.taskFail[taskName][hostName]+1
                else:
                    self.taskFail[taskName].update({hostName:1})
            else:
                self.taskFail[taskName]={hostName:1}
                    
        except Exception as e:
            Logger.exception(log)
        finally:
            self.lock.release()
            
    def updateTaksSent(self,taskName):
        try:
            self.lock.acquire()
            if taskName in self.taskSent:
                self.taskSent[taskName]= self.taskSent.get(taskName)+1
            else:
                self.taskSent[taskName]=1
        except Exception as e:
            Logger.exception(log)
        finally:
            self.lock.release()
            
    def updateTaskReceived(self,taskName,hostName):
        try:
            self.lock.acquire()
            if taskName in self.taskReceived:
                if hostName in self.taskReceived[taskName]:
                    self.taskReceived[taskName][hostName]=self.taskReceived[taskName][hostName]+1
                else:
                    self.taskReceived[taskName].update({hostName:1})
            else:
                self.taskReceived[taskName]={hostName:1}
                
        except Exception as e:
            Logger.exception(log)
        finally:
            self.lock.release()
    
    def updateTaskSucceeded(self,taskName,hostName,runTime,queueTime):
        try:
            self.lock.acquire()
            if taskName in self.taskSucceeded:
                if hostName in self.taskSucceeded[taskName]:
                    m= self.taskSucceeded[taskName][hostName]
                    m[TASK_COUNT]=m[TASK_COUNT]+1
                    m[TASK_RUNTIME]=m[TASK_RUNTIME]+runTime
                    m[TASK_QUEUE_TIME]=m[TASK_QUEUE_TIME]+queueTime
                else:
                    self.taskSucceeded[taskName].update({hostName:{TASK_COUNT:1,TASK_RUNTIME:runTime,TASK_QUEUE_TIME:queueTime}})
            else:
                self.taskSucceeded[taskName]={hostName:{TASK_COUNT:1,TASK_RUNTIME:runTime,TASK_QUEUE_TIME:queueTime}}
                
        except Exception as e:
            Logger.exception(log)
        finally:
            self.lock.release()
    
    def doAction(self,actionFun):
        sendDict=None
        receivedDict=None
        failDict=None
        succeedDict=None
        try:
            self.lock.acquire()
            sendDict = self.taskSent.copy()
            receivedDict = self.taskReceived.copy()
            failDict = self.taskFail.copy()
            succeedDict = self.taskSucceeded.copy()
            actionFun(sendDict,receivedDict,failDict,succeedDict)
            self.taskFail.clear()
            self.taskSent.clear()
            self.taskSucceeded.clear()
            self.taskReceived.clear()
        except Exception as e:
            Logger.exception(log)
        finally:
            self.lock.release()
    
cabbageCounter = CabbageCounter()

    
class CabbageCounterHolder():
    @classmethod
    def getCabbageCounter(cls):
        return cabbageCounter
    
    
