# -*- encoding: utf-8 -*-
'''
Created on 2016年8月1日

@author: hua
'''
from celery.app.base import Celery
# from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
# print CabbageHolder.getCabbage().ping("ubuntu")


# test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
# app = Celery('cabbage',backend="rpc://",broker=test)

server="amqp://cabbage_celery:cabbage_celery@10.0.137.88:5672/cabbage_vhost"

app = Celery('cabbage@utn-c-94.qihoo.net',broker=server)
        
print app.control.ping(timeout=5,destination=["celery@UTN-C-95.qihoo.net"])