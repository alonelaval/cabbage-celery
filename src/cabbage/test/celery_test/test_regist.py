# -*- encoding: utf-8 -*-
'''
Created on 2016年9月8日

@author: huawei
'''


from celery.app.base import Celery
from celery.app.task import Task
from celery.registry import tasks
import os
import threading
import time

test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
app = Celery('cabbage',backend="rpc://",broker=test)
        
def run():
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.current")
        os.environ.setdefault("DJANGO_PROJECT_DIR",
                              os.path.dirname(os.path.realpath(__file__)))
        app.worker_main()
        

class Hello(Task):
    send_error_emails = True

    def run(self, to):
        return 'hello {0}'.format(to)
    
if __name__=="__main__":
    t1 = threading.Thread(target=run)
    t1.setDaemon(True)
    t1.start()
    time.sleep(10)
    print "test"
    tasks.register(Hello)
    print "test2"
    t1.join()