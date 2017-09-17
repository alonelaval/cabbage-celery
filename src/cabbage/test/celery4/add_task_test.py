# -*- encoding: utf-8 -*-
'''
Created on 2017年7月14日

@author: huawei
'''
from celery import Celery

test ="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"
app = Celery('cabbage',backend="rpc://",broker=test)
        
# from celery import Task   
# from celery.registry import tasks
# 
# @app.task
# def add(x, y): 
#     return x + y
# 
# class Hello(Task):
#     queue = 'hipri'
# 
#     def run(self, to):
#         return 'hello {0}'.format(to)
# tasks.register(Hello)

if __name__ == '__main__':
#     app.config_from_object('cabbage.test.celery4.celeryconfig')
#     tasks.register(Hello)
    app.worker_main()