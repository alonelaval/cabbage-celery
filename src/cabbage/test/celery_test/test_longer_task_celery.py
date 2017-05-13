# -*- encoding: utf-8 -*-
'''
Created on 2016年5月31日

@author: hua
'''
from celery import Task, result
from celery.app.base import Celery
from celery.contrib.methods import task_method
from celery.events import EventReceiver, Events
from celery.events.state import State
from celery.exceptions import WorkerShutdown
from collections import OrderedDict
from cabbage.job.task import ITask
from scipy.lib.decorator import partial
from zope.interface.declarations import implementer
import ConfigParser
import multiprocessing
import os
import sys
import threading
import time
# if "/Users/hua/workspace/python/cabbage" not in sys.path:
#         sys.path.append("/Users/hua/workspace/python/cabbage")
#         sys.path.append("/Users/hua/workspace/python/cabbage/src")
        


cfg = ConfigParser.ConfigParser()
cfg.read(os.getcwd().split("cabbage")[0]+'cabbage/cabbage.cfg')



app = Celery('cabbage',backend="amqp",broker='amqp://172.16.4.134')
# app.config_from_object("cabbage.test.celery_test.celeryconfig")

@implementer(ITask)  
class T:
    def __init__(self):
        pass
    
#     @app.task(bind=True, filter=task_method,name="cabbage.test.test_celery.T.run")     
#     def run(self):
#         print "121212"
    
    @app.task(bind=True,filter=task_method,name="cabbage.test.test_celery.T.run2")     
    def run2(self,a,b):
        for i in range(10):
            time.sleep(5)
            print "dd"
        return a*b

        
def run():
#         os.environ['CELERYTEST_CONFIG_OBJECT'] = 'com.pingansec'
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.current")
        os.environ.setdefault("DJANGO_PROJECT_DIR",
                              os.path.dirname(os.path.realpath(__file__)))
#         os.environ.setdefault("CELERY_SEND_TASK_SENT_EVENT","True")
        
        app.conf.update(CELERY_SEND_TASK_SENT_EVENT =True,CELERY_SEND_EVENTS=True)
#         my_monitor(app)
        app.worker_main()
        

def test():
    t =T(1,2)
    t.run()
    
def shoudown():
    pass

if __name__=="__main__":
    
   
    t1 = threading.Thread(target=run)
    t1.setDaemon(True)
    t1.start()
    time.sleep(5)
    t1.join()
    


