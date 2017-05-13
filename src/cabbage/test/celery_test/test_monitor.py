# -*- encoding: utf-8 -*-
'''
Created on 2016年9月9日

@author: huawei
'''
from celery.app.base import Celery
from kombu.entity import Exchange,Queue

test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
app = Celery('cabbage',backend="rpc://",broker=test)

CELERY_QUEUES = ( Queue('mac', Exchange('mac'), routing_key='mac'),)
# 
# 
CELERY_ROUTES ={ u'test_both_task.TestBoth': {'queue': 'both', 'routing_key': 'both'}, u'test_mac_task.TestMacTask': {'queue': 'mac', 'routing_key': 'mac'}, u'test_ubuntu_task.TestUbuntuTask': {'queue': 'ubuntu', 'routing_key': 'ubuntu'}}
#  
app.conf.update(CELERY_QUEUES=CELERY_QUEUES)
app.conf.update(CELERY_ROUTES=CELERY_ROUTES)
app.conf.update(CELERY_SEND_TASK_SENT_EVENT=True,CELERY_SEND_EVENTS=True)

def my_monitor(app):
    state = app.events.State()
    
    def announce_failed_tasks(event):
        print "monitor"
#         print state.alive_workers()
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        if 'uuid' in event:
            task = state.tasks.get(event['uuid'])
            print task
        print event['type']
#         if event['type'] =='task-succeeded':
#             print event
#             task = state.tasks.get(event['uuid'])
#             print task
            
        
        
#         print event
#         print task
        

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                'task-sent':announce_failed_tasks,
                'task-received':announce_failed_tasks,
                'task-started':announce_failed_tasks,
                'task-succeeded':announce_failed_tasks,
                'task-failed':announce_failed_tasks,
                'task-revoked':announce_failed_tasks,
                'task-retried':announce_failed_tasks,
                'worker-online': announce_failed_tasks,
                'worker-offline': announce_failed_tasks,
#                 "*":announce_failed_tasks
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

my_monitor(app)

state = app.events.State()
print state.tasks.get('efa1363e-c3f7-4f7a-9d0e-8da5f71022d5')