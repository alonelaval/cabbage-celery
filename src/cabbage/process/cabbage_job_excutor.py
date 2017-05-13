# -*- encoding: utf-8 -*-
'''
Created on 2016年8月9日
 
@author: hua
'''
 
# from cabbage.event.handler.server_event_handler import \
#     jobRunHandler
# from cabbage.utils.util import singleton
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import JOB_EXECUTOR_COUNT, BASE
from cabbage.utils.util import singleton
from concurrent import futures
import Queue
import zope.event

log = Logger.getLogger(__name__)

def runJob(q):
    while True:
        try:
            evnet = q.get()
            zope.event.notify(evnet)
        except Exception:
            Logger.exception(log)
    
     
@singleton
class CabbageJobExecutor(object):
     
    def __init__(self):
        self.max = ConfigHolder.getConfig().getProperty(BASE,JOB_EXECUTOR_COUNT)
        self.executor =  futures.ThreadPoolExecutor(max_workers=int(self.max))
        self.jobQueue = Queue.Queue()
        for i in range(int(self.max)):
            self.executor.submit(runJob,self.jobQueue)
        
    def reload(self):
        self.executor.shutdown()
        self.executor =  futures.ThreadPoolExecutor(max_workers=ConfigHolder.getConfig().getProperty(BASE,JOB_EXECUTOR_COUNT))
     
    def addJobEvent(self,event):
        self.jobQueue.put(event)
 
class CabbageJobExecutorHolder():
    @classmethod
    def getCabbageJobExecutor(cls):
        return CabbageJobExecutor()