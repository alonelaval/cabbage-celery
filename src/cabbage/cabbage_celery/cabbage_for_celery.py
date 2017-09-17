# -*- encoding: utf-8 -*-
'''
Created on 2016年6月15日

@author: hua
'''
from celery.app.base import Celery
# from celery.contrib.methods import task_method
from cabbage.utils.host_name import HOST_NAME
import os
# from cabbage.utils.util import singleton

# app = Celery('cabbage',backend="rpc://",broker='amqp://172.16.4.134')

class CabbageCelery(Celery):
    def on_init(self):
        pass
# @singleton

class Cabbage():
    def __init__(self,hostName=HOST_NAME,backend="rpc://",broker='amqp://172.16.4.134'):
        self.hostName=hostName
        self.backend=backend
        self.broker=broker
        self.app = CabbageCelery('cabbage',broker=broker)
#         os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.current")
#         os.environ.setdefault("DJANGO_PROJECT_DIR",
#                               os.path.dirname(os.path.realpath(__file__)))
        self.app.config_from_object('cabbage.cabbage_celery.celeryconfig')
       
    def register_task(self,taskObj):
        self.app.register_task(taskObj)
        
    def start(self):
        argv =['worker',
               '--without-mingle',
               '--without-gossip',
#                '--without-heartbeat'
            '--loglevel=info'
               ]
        self.app.worker_main(argv)
    
    def restart(self):
        argv =['--autoreload']
        self.app.worker_main(argv)
    
#     @DeprecationWarning
#     def addTask(self,fun,name=None):
#         if name:
#             name=fun.name
#         @self.app.task(bind=True,filter=task_method,name=name)
#         def f(fun):
#             return fun
#         
    def taskList(self):
        return self.app.tasks().items()
    
    def removeTask(self,task):
        pass
    
    def revokeTask(self,taskId):
        self.app.control.revoke(taskId, terminate=True)
    
    def getApp(self):
        return self.app
    
    def ping(self,hostName=HOST_NAME):
#         print hostName
        return self.app.control.ping(timeout=5,destination=["celery@%s"%hostName])
    #add is alive
    def workIsAlive(self,hostName):
        if len(self.ping(hostName)) >0:
            return True
        
        return False
    #all revokeByTaskName
    def revokeByTaskName(self,taskName):
        self.app.control.revoke([uuid for uuid, _ in self.app.events.State().tasks_by_type(taskName)])
    
    def stop(self,hostName=HOST_NAME):
#         self.app.close()
#         print hostName
        
        self.app.control.broadcast("shutdown", destination=["celery@%s"%hostName])
        


