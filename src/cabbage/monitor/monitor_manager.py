# -*- encoding: utf-8 -*-
'''
Created on 2016年9月9日

@author: huawei
'''
from cabbage.constants import TASK_FAILED, TASK_SUCCEEDED, \
    TASK_SENT, TASK_STARTED, WORKER_ONLINE, WORKER_OFFLINE, TASK_RECEIVED, \
    TASK_REVOKED, TASK_RETRIED
from concurrent import futures
import threading

class MonitorManager(object):
    def __init__(self):
        self.executor =  futures.ThreadPoolExecutor(max_workers=20)
        self.store={
                TASK_FAILED:set(),
                TASK_SUCCEEDED:set(),
                TASK_SENT   :set(),
                TASK_STARTED:set(),
                WORKER_ONLINE:set(),
                WORKER_OFFLINE:set(),
                TASK_RECEIVED:set(),
                TASK_REVOKED:set(),
                TASK_RETRIED:set(),
                 }
    def register(self,fun,tp):
        lock =threading.RLock()
        try:
            lock.acquire()
            self.store[tp].add(fun)
        finally:
            lock.release()
    def unregister(self,fun,tp):
        lock =threading.RLock()
        try:
            lock.acquire()
            self.store[tp].remove(fun)
        finally:
            lock.release()
            
    def fire(self,tp,state,event,app):
        for f in self.store[tp]:
            self.executor.submit(f,state,event,app)
            
monitorManager = MonitorManager()