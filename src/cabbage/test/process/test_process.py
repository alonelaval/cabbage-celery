# -*- encoding: utf-8 -*-
'''
Created on 2016年10月12日

@author: huawei
'''
import multiprocessing
import os
import tornado.ioloop
def action(queue):
    while True:
        i = queue.get()
        if i :
            print os.getpid()
    
class JobUploadPool():
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.jobIdQueue =self.manager.Queue()
        self.start()
    def add(self,jobId):
        self.jobIdQueue.put(jobId)
        
    def start(self):
        jobProcessCount = 10
        self.pool = multiprocessing.Pool(processes =int(jobProcessCount))
        for i in range(jobProcessCount):
            self.pool.apply_async(action,(self.jobIdQueue,))
    
test = JobUploadPool()
        
for i in range(100):
    test.add(1)
    
test.start()
tornado.ioloop.IOLoop.current().start()
