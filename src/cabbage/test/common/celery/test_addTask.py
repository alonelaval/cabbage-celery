# -*- encoding: utf-8 -*-
'''
Created on 2016年7月12日

@author: hua
'''
from celery import bootsteps
from celery.app import control
from celery.app.control import Control
from celery.worker import consumer
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.cabbage.util import isCabbageTask, \
    isCabbageMain
from cabbage.common.file.load_file_holder import LoadMoudleHolder
from cabbage.config import ConfigHolder
from cabbage.constants import PYTHON, BASE, CLIENT_FILE_DIRECTORY
from cabbage.data.zookeeper_store import ZookeeperStore
import threading
import time
import unittest

def run():
    CabbageHolder.getCabbage().start()
    print "shutdown t1"

def restart():
    CabbageHolder.getCabbage().restart()
    print "shutdown restart"

class ConsumerStep(bootsteps.StartStopStep):
    requires = ('celery.worker.consumer:Tasks',)
    def __init__(self, parent, **kwargs):
        # here we can prepare the Worker/Consumer object
        # in any way we want, set attribute defaults and so on.
        print('{0!r} is in init'.format(parent))

    def start(self, parent):
        # our step is started together with all other Worker/Consumer
        # bootsteps.
        print('{0!r} is starting'.format(parent))

    def stop(self, parent):
        # the Consumer calls stop every time the consumer is restarted
        # (i.e. connection is lost) and also at shutdown.  The Worker
        # will call stop at shutdown only.
        print('{0!r} is stopping'.format(parent))

    def shutdown(self, parent):
        # shutdown is called by the Consumer at shutdown, it's not
        # called by Worker.
        print('{0!r} is shutting down'.format(parent))

class Consumer(consumer.Consumer):
    def __init__(self, app):
        self.app = app

class TestAddTask(unittest.TestCase):
    def setUp(self):
        self.app = CabbageHolder.getCabbage().getApp()
        self.t1 = threading.Thread(target=run)
        self.t1.setDaemon(True)
        self.t1.start()
        time.sleep(2)
    
    def test_aaa(self):
#         time.sleep(10)
#         self.app.control.broadcast("shutdown", destination=["celery@huamac"])
#         time.sleep(10)
        
#         store=ZookeeperStore()
#         jobId="123456789"
#         job = store.getJob(jobId)
        loadMoudle = LoadMoudleHolder.getLoadMoudle(PYTHON)
#         clientDir = ConfigHolder.getConfig().getProperty(BASE,CLIENT_FILE_DIRECTORY)
#         path = clientDir+"/"+jobId
#         print path
#         print job.fileName
        path="/Users/hua/workspace/python/cabbage/client_file_path/123456789"
        import sys
        sys.path.append(path)
        classes =loadMoudle.load("/Users/hua/workspace/python/cabbage/client_file_path/123456789","test_main.py")
        classes2 =loadMoudle.load("/Users/hua/workspace/python/cabbage/client_file_path/1234567890","test_task1.py")
#         classes2 =loadMoudle.load(path,"test_main.py")
#         self.t2 = threading.Thread(target=restart)
#         self.t2.setDaemon(True)
#         self.t2.start()
#         print classes
        for clazz in classes:
            obj = clazz[1]
            print obj
          
#             if isCabbageTask(obj):
#                 cabbage = CabbageHolder.getCabbage()
#                 cabbage.addTask(obj.run)
               
            if isCabbageMain(obj):
                m = obj
#           for celery.app.registry
#         self.app.close()
#         
#         self.app.control.broadcast("shutdown", destination=["celery@huamac"])
        for clazz in classes2:
            obj = clazz[1]
            print obj
          
#             if isCabbageTask(obj):
#                 cabbage = CabbageHolder.getCabbage()
#                 cabbage.addTask(obj.run)
               
            if isCabbageMain(obj):
                m2 = obj
        
# #        
#         mos = self.app.conf["CELERY_IMPORTS"]
#             
#         m =("test_task.TestTask",)
#         
#         self.app.conf["CELERY_IMPORTS"]=mos+m
#         print "CELERY_IMPORTS %s" % self.app.conf["CELERY_IMPORTS"]
#         
        i = self.app.control.inspect()
        result = i.stats()
        print result
        print i.registered_tasks()
#         self.app.control.broadcast('pool_restart', arguments={'reload': True})
#         self.app.control.add_consumer("test_task.TestTask")
        
#         print self.app.user_options
#         consumer = Consumer(self.app)
#         consumer.update_strategies()
       
#         self.app.send_task("test_task.TestTask", args=[1,2])
        
      
       
        
      
#         celery.worker.consumer:Tasks
        m().run()
        m2().run()
#         from celery.task.control import  inspect
#         i = inspect()
#         i.registered_tasks()
        
#         print classes2
#         for clazz in classes2:
#             if isCabbageMain(clazz[1]):
#                 print 1112
#                 clazz[1]().run()

        
        self.t1.join()
        
        
if __name__=="__main__":
    unittest.main()
