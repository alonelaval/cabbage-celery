# -*- encoding: utf-8 -*-
'''
Created on 2016年9月9日

@author: huawei
'''
from celery.app.base import Celery
# from kombu.entity import Exchange,Queue

app = Celery('cabbage',backend="rpc://",broker='amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost')
# app.config_from_object("cabbage.cabbage_celery.celeryconfig")
# app.conf.update(CELERY_QUEUES = ( Queue('test', Exchange('test'), routing_key='test'), Queue('test2', Exchange('test2'), routing_key='test2')),
#                 {u'test_both_task.TestBothTask': {'queue': 'both', 'routing_key': 'both'}, u'test_both_task.TestBoth': {'queue': 'both', 'routing_key': 'both'}, u'test_mac_task.TestMacTask': {'queue': 'mac', 'routing_key': 'mac'}, u'test_ubuntu_task.TestUbuntuTask': {'queue': 'ubuntu', 'routing_key': 'ubuntu'}}
#                 )
# 
#  
# CELERY_QUEUES = ( Queue('celery', Exchange('celery'), routing_key='celery'),)
# 
# 
# CELERY_ROUTES ={u'test_both_task.TestBothTask': {'queue': 'both', 'routing_key': 'both'}, u'test_both_task.TestBoth': {'queue': 'both', 'routing_key': 'both'}, u'test_mac_task.TestMacTask': {'queue': 'mac', 'routing_key': 'mac'}, u'test_ubuntu_task.TestUbuntuTask': {'queue': 'ubuntu', 'routing_key': 'ubuntu'}}
#  
# app.conf.update(CELERY_ROUTES=CELERY_ROUTES)
# 
# CELERY_QUEUES = ( Queue('default', Exchange('default'), routing_key='default'),
# )

def my_monitor(app):
    state = app.events.State()
    
    def announce_failed_tasks(event):
        state.event(event)
        print "monitor"
        print state.alive_workers()
        print event
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        if 'uuid' in event:
            task = state.tasks.get(event['uuid'])
            print task
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
                "*":announce_failed_tasks
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

my_monitor(app)

# state = app.events.State()
# print state.tasks.get('efa1363e-c3f7-4f7a-9d0e-8da5f71022d5')