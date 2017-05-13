# -*- encoding: utf-8 -*-
'''
Created on 2016年9月6日

@author: huawei
'''
from celery.app.base import Celery
from cabbage.utils.host_name import getHostName
test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
#server="amqp://cabbage_celery:cabbage_celery@10.0.137.88:5672/cabbage_vhost"

app = Celery('cabbage',backend="rpc://",broker=test)
# celeryconfig.CELERY_QUEUES =  ( Queue('default', Exchange('default'), routing_key='default'),
#                    Queue('cabbage', Exchange('cabbage'), routing_key='cabbage'))
# app.config_from_object('cabbage.test.celery_test.celeryconfig')
# app.worker_main()
ubuntu="ubuntu"
print app.control.ping(timeout=2,destination=["celery@%s"%ubuntu])
print app.control.broadcast("shutdown", destination=["celery@%s"%ubuntu])