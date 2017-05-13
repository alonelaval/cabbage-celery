# -*- encoding: utf-8 -*-
'''
Created on 2016年9月23日

@author: huawei
'''
from celery.app.base import Celery
app = Celery('cabbage',backend="amqp",broker='amqp://172.16.4.134')


app.control.broadcast("shutdown", destination=["celery@huamac"])

