# -*- encoding: utf-8 -*-
'''
Created on 2016年7月25日

@author: hua
'''
# -*- encoding: utf-8 -*-
'''
Created on 2016年7月12日

@author: hua
'''
# from celery import bootsteps
# from celery.app import control
# from celery.app.control import Control
# from celery.worker import consumer
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.cabbage.util import isCabbageTask, \
    isCabbageMain
from cabbage.common.file.load_file_holder import LoadMoudleHolder
from cabbage.config import ConfigHolder
from cabbage.constants import PYTHON, BASE, CLIENT_FILE_DIRECTORY
from cabbage.data.zookeeper_store import ZookeeperStore
import multiprocessing
import os
import threading
import time
import unittest

def run():
    CabbageHolder.getCabbage().start()
    print "shutdown t1"

def restart():
    CabbageHolder.getCabbage().restart()
    print "shutdown restart"

class TestAddTask(unittest.TestCase):
    def setUp(self):
        pass
#         self.p1 = multiprocessing.Process(target = worker_start)
#         self.p1.start()
#         time.sleep(3)
    
    def test_aaa(self):
        p2 = multiprocessing.Process(target = run)
        p2.start()
        
#         t1 = threading.Thread(target=run)
#         t1.setDaemon(True)
#         t1.start()
            
        loadMoudle = LoadMoudleHolder.getLoadMoudle(PYTHON)
    #         clientDir = ConfigHolder.getConfig().getProperty(BASE,CLIENT_FILE_DIRECTORY)
    #         path = clientDir+"/"+jobId
    #         print path
    #         print job.fileName
        path="/Users/hua/workspace/python/cabbage/client_file_path/123456789"
        import sys
        sys.path.append(path)
        classes =loadMoudle.load(path,"test_task.py")
        classes2 =loadMoudle.load("/Users/hua/workspace/python/cabbage/client_file_path/1234567890","test_task1.py")
        
        time.sleep(5)
        CabbageHolder.getCabbage().stop(hostName="celery@huamac")
        print "end"
        p2.join()
        
        print "start"
#         t2 = threading.Thread(target=run)
#         t2.setDaemon(True)
#         t2.start()
        
        p2 = multiprocessing.Process(target = run)
        p2.start()
       
        p2.join()   

    
def worker_start():
    print "worker_start:%d" % os.getpid()
    
    t1 = threading.Thread(target=run)
    t1.setDaemon(True)
    t1.start()
        
    loadMoudle = LoadMoudleHolder.getLoadMoudle(PYTHON)
#         clientDir = ConfigHolder.getConfig().getProperty(BASE,CLIENT_FILE_DIRECTORY)
#         path = clientDir+"/"+jobId
#         print path
#         print job.fileName
    path="/Users/hua/workspace/python/cabbage/client_file_path/123456789"
    import sys
    sys.path.append(path)
    classes =loadMoudle.load(path,"test_task.py")
    classes2 =loadMoudle.load("/Users/hua/workspace/python/cabbage/client_file_path/1234567890","test_task1.py")
    print "worker_start:finish"
    t1.join()
    
# def worker():
#     print "worker_pid:%d"% os.getpid()
#     app=CabbageHolder.getCabbage().getApp()
#     i = app.control.inspect()
#     result = i.stats()
#     print result
#     print i.registered_tasks()
#     loadMoudle = LoadMoudleHolder.getLoadMoudle(PYTHON)
#     import sys
#     path="/Users/hua/workspace/python/cabbage/client_file_path/123456789"
#     sys.path.append(path)
#     classes =loadMoudle.load(path,"test_main.py")
#     
#     for clazz in classes:
#         obj = clazz[1]
#         if isCabbageMain(obj):
#                 m = obj
#                 m().run()
        
if __name__=="__main__":
    unittest.main()
    
