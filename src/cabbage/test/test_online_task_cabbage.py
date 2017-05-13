# -*- encoding: utf-8 -*-
'''
Created on 2016年8月10日

@author: hua
'''
from celery.app.base import Celery



app = Celery('cabbage',backend="rpc://",broker='amqp://cabbage_celery:cabbage_celery@10.0.137.88:5672/cabbage_vhost')


for i in range(1):
        result= app.send_task("product_list_crawler.ProductListCrawlerTask",kwargs={'lid': 1})
        print result

# print "start job"
# i = app.control.inspect()
# result = i.stats()
# print result
# print i.registered_tasks()