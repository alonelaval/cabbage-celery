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
app.config_from_object("cabbage.test.celery_test.celeryconfig")

@implementer(ITask)  
class T:
    def __init__(self):
        pass
    
    @app.task(bind=True, filter=task_method,name="cabbage.test.test_celery.T.run")     
    def run(self):
        print "121212"
    
    @app.task(bind=True,filter=task_method,name="cabbage.test.test_celery.T.run2")     
    def run2(self,a,b):
        print "121212"
        return a*b

class T2(Task):
    def run(self):
        pass
    
class Test():
    def run(self):
        for i in range(100):
#             result = T.run.delay()
            result2 = T.run2.apply_async(args=(4, 5));
#             result2 = T.run2.delay(4, 5)
            print "result2:"+str(result2)
            while(1):
                time.sleep(5)
                if result2.ready():
                    print result2.status
                    print "result2:"+str(result2.result)
                    break
                print result2.status
        print ITask.implementedBy(T) 
        
def run():
#         os.environ['CELERYTEST_CONFIG_OBJECT'] = 'com.pingansec'
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.current")
        os.environ.setdefault("DJANGO_PROJECT_DIR",
                              os.path.dirname(os.path.realpath(__file__)))
#         os.environ.setdefault("CELERY_SEND_TASK_SENT_EVENT","True")
        
        app.conf.update(CELERY_SEND_TASK_SENT_EVENT =True,CELERY_SEND_EVENTS=True)
#         my_monitor(app)
        app.worker_main()
        
def my_monitor(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
#         task = state.tasks.get(event['uuid'])
        print "monitor"
        print event
#         print task

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                'task-sent':announce_failed_tasks,
                'task-received':announce_failed_tasks,
                'task-started':announce_failed_tasks,
                'task-succeeded':announce_failed_tasks,
                'task-revoked':announce_failed_tasks,
                'task-retried':announce_failed_tasks,
                'worker-online': announce_failed_tasks,
                'worker-offline': announce_failed_tasks,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)
    
def test():
    t = Test()
    t.run()
    t =T(1,2)
    t.run()
def shoudown():
    pass

# def my_monitor(app):
#     state = app.events.State()
# 
#     def announce_failed_tasks(event):
#         state.event(event)
#         # task name is sent only with -received event, and state
#         # will keep track of this for us.
#         task = state.tasks.get(event['uuid'])
# 
#         print('TASK FAILED: %s[%s] %s' % (
#             task.name, task.uuid, task.info(), ))
# 
#     with app.connection() as connection:
#         recv = app.events.Receiver(connection, handlers={
#                 'task-failed': announce_failed_tasks,
#                 '*': state.event,
#         })
#         recv.capture(limit=None, timeout=None, wakeup=True)
        
def event():
#     print event
#     e =Events(app)
#     print e.State().tasks.keys()
#     print e.State().alive_workers()
#     print event
    my_monitor(app)
# def event():
#     with app.connection() as conn:
#         recv = EventReceiver(conn,
#                              handlers={"*": on_event},
#                              app=app)
#         
#         recv.capture(limit=None, timeout=None, wakeup=True)
    
if __name__=="__main__":
    
   
    t1 = threading.Thread(target=run)
    t1.setDaemon(True)
    t1.start()
    time.sleep(5)
    t1.join()
#     t2=threading.Thread(target=event)
#     t2.setDaemon(True)
#     t2.start()
#     
#     p = multiprocessing.Process(target = test)
#     p.start()
#     p.join()
# #     state = State()
#     time.sleep(5)
#     print "asdfasdf",state.alive_workers()
#     print "asdfasdf",state.tasks
    
#     worker =app.Worker()
#     print worker
#     print worker.tasklist()
#     from celery.events import Event
#     ev = Event('worker-online',hostname="celery@huamac")
#     r =state.event(ev)
#     print state.alive_workers()
#             Event('worker-offline', hostname='utest1')
#     worker.terminate(in_sighandler=True)
#     my_monitor(app)
#     from celery.worker import state
#     state.should_stop=True
#     try:
#         state.maybe_shutdown()
#     except WorkerShutdown:
#         state.maybe_shutdown()
#         print 111
    
#     i = app.control.inspect()
#     result = i.stats()
#     print result.items()




#     app.control.broadcast("shutdown", destination=["celery@huamac"])
#     print app.control.inspect()
#     print app.control.ping(timeout=0.5)
#     a = OrderedDict()
#     for name, worker in state.workers.items():
#         print name,worker
#     t1.join()
    
    


