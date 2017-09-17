# -*- encoding: utf-8 -*-
'''
Created on 2017年7月22日

@author: huawei
'''
from cabbage.test.celery4.myapp import DebugTask
from celery import Celery, Task
from test_mac_task import TestMacTask

test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
app = Celery(
    'myapp',
    broker=test,
    # ## add result backend here if needed.
    # backend='rpc'
)
# TestMacTask.bind(app)
# # DebugTask.bind(app)
# obj  = TestMacTask()
# result = obj.apply_async((1,2,1),expires=5)
# app.register_task(obj)
# result =obj.apply_async()
# print result
# app.register_task(debugTask)
# @app.task
# def aa():
#     pass
# task_queues = {
#     'celery': {
#         'exchange': 'celery',
#         'routing_key': 'celery',
#     },
# }
# 
# task_routes = {
#     'myapp.DebugTask ': {
#         'queue': 'defalut',
#         'routing_key': 'defalut',
#     },
# }
# app.config_from_object('cabbage.test.celery4.celeryconfig')
# app.conf.task_routes = task_routes
# app.conf.task_queues = task_queues
app.conf.update(CELERY_ROUTES = {   
                    u'test_mac_task.TestMacTask': {'queue': 'test', 'routing_key': 'test', 'exchange': 'test'}
                   # 'test_mac_task.TestMacTask': {'queue': 'test', 'routing_key': 'test'}                     
#                  'myapp.DebugTask': {'queue': 'celery', 'routing_key': 'celery','exchange':'celery'},     
#                  'product_list_crawler.ProductListCrawlerTask': {'queue': 'celery', 'routing_key': 'celery'}
                  })
#-----------------
# result = app.send_task("test_mac_task.TestMacTask")
# print result

#---------------

TestMacTask.bind(app)
# DebugTask.bind(app)
obj  = TestMacTask()
# app.register_task(obj)
result = obj.apply_async((1,2,1),expires=5)

