# -*- encoding: utf-8 -*-
'''
Created on 2016年8月10日

@author: hua
'''
from celery.app.base import Celery
from celery.contrib.methods import task_method
from cabbage.job.task import ITask
from zope.interface.declarations import implementer
import os
import threading
import time

app = Celery('cabbage',backend="rpc://",broker='amqp://172.16.4.134')
# 
# @implementer(ITask)  
# class T:
#     def __init__(self):
#         pass
#     
#     @app.task(bind=True, filter=task_method,name="cabbage.test.test_celery.T.run")     
#     def run(self):
#         print "121212"
#     
#     @app.task(bind=True,filter=task_method,name="cabbage.test.test_celery.T.run2")     
#     def run2(self,a,b,no):
#         print "NO:%s"%no
#         time.sleep(5)
#         return a*b


def run():
#         os.environ['CELERYTEST_CONFIG_OBJECT'] = 'com.pingansec'
#         os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.current")
#         os.environ.setdefault("DJANGO_PROJECT_DIR",
#                               os.path.dirname(os.path.realpath(__file__)))

        argv =['--pool=threads']
        app.worker_main(argv)
        
class Test():
    def run(self):
        for i in range(100):
#             result = T.run.delay()
            result2 = T.run2.delay(4, 5,i);
#             result2 = T.run2.delay(4, 5)
            print "result2:"+str(result2)
            while(1):
                if result2.ready():
                    print result2.result
                    break
                time.sleep(2)
                print result2.status
#         print ITask.implementedBy(T) 
        
if __name__=="__main__":
    for i in range(100):
        result= app.send_task("test_task.TestTask", args=(1,2))
        print result.get()
#     t1 = threading.Thread(target=run)
#     t1.setDaemon(True)
#     t1.start()
#     time.sleep(5)
#     Test().run()
    
    
    