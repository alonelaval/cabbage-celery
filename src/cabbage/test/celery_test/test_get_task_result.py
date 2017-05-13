# -*- encoding: utf-8 -*-
'''
Created on 2016年10月13日

@author: huawei
'''

from celery.app.base import Celery
from celery.result import AsyncResult
from kombu.entity import Queue, Exchange
import time

# from test_nfs_task import TestNfsTask

test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
app = Celery('cabbage',broker=test)
app.config_from_object("cabbage.cabbage_celery.celeryconfig")
# import celeryconfig
# app.config_from_object(celeryconfig)


for k,v in app.conf.items():
    print k,v
app.conf.update(CELERY_ROUTES = {     
                 'test_ic_task.TestIcTask': {'queue': 'test2', 'routing_key': 'test2'},     
#                  'product_list_crawler.ProductListCrawlerTask': {'queue': 'celery', 'routing_key': 'celery'}
                  })
# taskId = "de1d0b16-57b1-4128-87bc-3697f78ab6dc"

state = app.events.State()
print app.tasks()

# print state.tasks.get(taskId)

app.send_task("test_ic_task.TestIcTask",kwargs={"jobId"})

res =AsyncResult(taskId)
print res._get_task_meta()
print res.ready()
print res.result
print dir(res)
print res.task_name