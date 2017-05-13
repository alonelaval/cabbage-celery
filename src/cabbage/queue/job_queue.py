# -*- encoding: utf-8 -*-
'''
Created on 2016年7月25日

@author: hua
'''
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, JOB_PROCESS_COUNT
from cabbage.utils.util import singleton
import multiprocessing
# 
#              zope.event.notify(JobRunEvent(jobId,params))


#@deprecated              
@singleton
class JobEventPool():
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.jobEventQueue =self.manager.Queue()
        
    def add(self,jobEvent):
        print jobEvent 
        try:
            import cPickle as pickle
        except ImportError:
            import pickle
#         print pickle.dumps(jobEvent)
        self.jobEventQueue.put(pickle.dumps(jobEvent))
        
    def start(self):
        jobProcessCount = ConfigHolder.getConfig().getProperty(BASE,JOB_PROCESS_COUNT)
        self.pool = multiprocessing.Pool(processes =int(jobProcessCount))
        for i in range(int(jobProcessCount)):
            self.pool.apply(self.runEvent,(self.jobEventQueue,))
        
    def runEvent(self,queue):
        while True:
            jobEvent = queue.get(False)
            if jobEvent:
                print jobEvent
                
class JobEventPoolHolder():
    @classmethod
    def getJobEventPool(self):
        return JobEventPool()
