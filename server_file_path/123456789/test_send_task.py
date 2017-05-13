# -*- encoding: utf-8 -*-
'''
Created on 2016年9月7日

@author: huawei
'''
from celery.app.base import Celery
from kombu.entity import Queue, Exchange
import time
from test_hdfs_task import TestHdfsTask


test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
app = Celery('cabbage',broker=test)
app.config_from_object("cabbage.cabbage_celery.celeryconfig")
# import celeryconfig
# app.config_from_object(celeryconfig)


# for k,v in app.conf.items():
#     print k,v
app.conf.update(CELERY_ROUTES = {     
                 'test_hdfs_task.TestHdfsTask': {'queue': 'hdfs', 'routing_key': 'hdfs'},     
#                  'product_list_crawler.ProductListCrawlerTask': {'queue': 'celery', 'routing_key': 'celery'}
                  })
app.conf.update(CELERY_QUEUES=( Queue('hdfs', Exchange('hdfs'), routing_key='hdfs'),))
print app.conf["CELERY_ACCEPT_CONTENT"]
print app.conf["CELERY_RESULT_BACKEND"]
# app.conf.update(CELERY_ACCEPT_CONTENT = ['json'],CELERY_TASK_SERIALIZER = 'json',CELERY_RESULT_SERIALIZER = 'json')

results = []
for i in range(2):
#         result= app.send_task("test_hdfs_task.TestHdfsTask",kwargs={"jobId":"job-61d72e47-8323-4144-9e37-957679bc98ce"})
        TestHdfsTask.bind(app)
        task = TestHdfsTask()
        result = task.apply_async(args=[1,2],kwargs={"jobId":"job-61d72e47-8323-4144-9e37-957679bc98ce"},expires=5)
        task
        time.sleep(1)
        results.append(result)

while 1:
    time.sleep(1)
#     from celery.task.control import inspect
#     i = inspect()
#     print i.scheduled()
#     print i.active()
    for result in results:
#         print result.backend
#         print result.get()
        print result      
        print result.status
        print result.result 
