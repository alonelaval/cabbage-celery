# -*- encoding: utf-8 -*-
'''
Created on 2016年9月8日

@author: huawei
'''


from celery import Task
from celery import Celery
import os
import threading
import time

# from celery.registry import tasks

class Hello(Task):
    send_error_emails = True
    def run(self,to):
        print to
        
test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
app = Celery('cabbage',backend="rpc://",broker=test)
        

@app.task
def run1(a,to):
        return 'hello {0}'.format(to)


class NaiveAuthenticateServer(Task):

    def __init__(self):
        self.users = {'george': 'password'}

    def run(self, username, password):
        try:
            return self.users[username] == password
        except KeyError:
            return False
    
def run():
        Hello()
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.current")
        os.environ.setdefault("DJANGO_PROJECT_DIR",
                              os.path.dirname(os.path.realpath(__file__)))
        app.worker_main()
        


    
if __name__=="__main__":
    t1 = threading.Thread(target=run)
    t1.setDaemon(True)
    t1.start()
    time.sleep(10)
    print "test"
#     tasks.register(Hello)
    print "test2"
    t1.join()