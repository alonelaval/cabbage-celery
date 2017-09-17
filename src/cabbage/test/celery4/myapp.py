# -*- encoding: utf-8 -*-
'''
Created on 2017年7月15日

@author: huawei
'''
from __future__ import absolute_import, unicode_literals
from celery import Celery, Task
from celery.app.registry import TaskRegistry
import sys


class DebugTask(Task):
#     def __init__(self):
#         self.name = self.__name__
#         print self.__class__
        
    def __call__(self, *args, **kwargs):
        print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)
    
    def run(self):
        print "hello world"
        return 1

debugTask = DebugTask()
# print debugTask.name
# taskRegistry = TaskRegistry()
# taskRegistry.register(debugTask)

test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
app = Celery(
    'myapp',
    broker=test,
    # ## add result backend here if needed.
    # backend='rpc'
)
app.register_task(debugTask)
# 
# app.autodiscover_tasks(packages=['cabbage.test.celery4.task.test_mac_task'])

# @app.task
# def add(x, y):
#     return x + y

if __name__ == '__main__':
    print dir()
    import cabbage.test.celery4.add_task_test
    print 
    argv =['worker',
               '--without-mingle',
               '--without-gossip',
#                '--without-heartbeat'
                '--loglevel=debug'
               ]
    app.config_from_object('cabbage.test.celery4.celeryconfig')
    app.worker_main(argv)