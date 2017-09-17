# -*- encoding: utf-8 -*-
'''
Created on 2016年7月13日

@author: hua
'''
from cabbage.config import ConfigHolder
from cabbage.constants import BASE
from cabbage.utils.host_name import HOST_NAME, LOCAL_IP
from kombu.entity import Exchange, Queue

# CELERYD_POOL_RESTARTS = True
CELERY_ALWAYS_EAGER=False

CELERYD_LOG_LEVEL="INFO"
#CELERY_REDIRECT_STDOUTS_LEVEL="DEBUG"

if ConfigHolder.getConfig().hasProperty(BASE,"celerydConcurrency"):
    CELERYD_CONCURRENCY=ConfigHolder.getConfig().getProperty(BASE, "celerydConcurrency")
else:
    CELERYD_CONCURRENCY=1

CELERY_IGNORE_RESULT = True

# CELERY_TRACK_STARTED =True

CELERY_SEND_TASK_SENT_EVENT =True

CELERY_SEND_EVENTS=True
 
#CELERY_RESULT_BACKEND = 'amqp'
#CELERY_RESULT_EXCHANGE = 'celereyResults'

 
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# from kombu import serialization
# serialization.registry._decoders.pop("application/x-python-serialize")
#CELERY_IGNORE_RESULT = False # this is less important
 
BROKER_HEARTBEAT = 0

# CELERY_QUEUES = ( Queue('celery', Exchange('celery'), routing_key='celery'),)

CELERYD_MAX_TASKS_PER_CHILD=40

CELERY_ROUTES = {}

CELERYD_LOG_FORMAT="[%(asctime)s: %(levelname)s/"+HOST_NAME+":"+LOCAL_IP+"/%(processName)s] %(message)s"
#print "[%(asctime)s: %(levelname)s/"+getHostName()+"/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s"
CELERYD_TASK_LOG_FORMAT= "[%(asctime)s: %(levelname)s/"+HOST_NAME+":"+LOCAL_IP+"/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s"
# 
# CELERY_QUEUES = ( Queue('default', Exchange('default'), routing_key='default'),
# )
