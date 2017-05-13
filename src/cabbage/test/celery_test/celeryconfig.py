# -*- encoding: utf-8 -*-
'''
Created on 2016年7月13日

@author: hua
'''
from kombu.entity import Exchange,Queue

# CELERYD_POOL_RESTARTS = True
# CELERY_ALWAYS_EAGER=False

CELERYD_LOG_LEVEL="INFO"
#CELERY_REDIRECT_STDOUTS_LEVEL="DEBUG"

CELERYD_CONCURRENCY=8
# CELERY_IGNORE_RESULT

# CELERY_TRACK_STARTED =True
# 
CELERY_SEND_TASK_SENT_EVENT =True
 
CELERY_SEND_EVENTS=True
  
CELERY_RESULT_BACKEND = 'rpc'
  
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# from kombu import serialization
# serialization.registry._decoders.pop("application/x-python-serialize")
CELERY_IGNORE_RESULT = False # this is less important
  
  
CELERY_QUEUES = ( Queue('celery', Exchange('celery'), routing_key='celery'),)
# 
# 
# 
# # 
# # CELERY_QUEUES = ( Queue('default', Exchange('default'), routing_key='default'),
# # )