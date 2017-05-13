# -*- encoding: utf-8 -*-
'''
Created on 2016年9月5日

@author: huawei
'''
from celery.app.base import Celery
# from cabbage.test.celery_test import celeryconfig
from kombu.entity import Queue, Exchange


test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
#server="amqp://cabbage_celery:cabbage_celery@10.0.137.88:5672/cabbage_vhost"

app = Celery('aaa',backend="rpc://",broker=test)
# celeryconfig.CELERY_QUEUES =  ( Queue('default', Exchange('default'), routing_key='default'),
#                    Queue('cabbage', Exchange('cabbage'), routing_key='cabbage'))
app.config_from_object('cabbage.test.celery_test.celeryconfig')
app.worker_main()