# -*- encoding: utf-8 -*-
'''
Created on 2016年9月7日

@author: huawei
'''
from celery.app.base import Celery
from kombu.entity import Queue, Exchange
import time


test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
app = Celery('cabbage',broker=test)
app.config_from_object("cabbage.cabbage_celery.celeryconfig")
# import celeryconfig
# app.config_from_object(celeryconfig)


# for k,v in app.conf.items():
#     print k,v
app.conf.update(CELERY_ROUTES = {     
                 'test_nfs_task.TestNfsTask': {'queue': 'test', 'routing_key': 'test'},     
#                  'product_list_crawler.ProductListCrawlerTask': {'queue': 'celery', 'routing_key': 'celery'}
                  })
# app.conf.update(CELERY_QUEUES=( Queue('hdfs', Exchange('hdfs'), routing_key='hdfs'),))
# print app.conf["CELERY_RESULT_BACKEND"]
results = []
for i in range(10000):
    print i
    result= app.send_task("test_nfs_task.TestNfsTask",kwargs={"jobId":"job-a986d7d9-4950-4c45-a3c5-6553d81d5a36","no":i})
    results.append(result)

time.sleep(10)
#     from celery.task.control import inspect
#     i = inspect()
#     print i.scheduled()
#     print i.active()
# for result in results:
# #         print result.backend
# #         print result.get()
#     print result      
#     print result.status
#     print result.result 
