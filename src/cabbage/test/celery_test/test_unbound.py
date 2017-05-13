# -*- encoding: utf-8 -*-
'''
Created on 2016年9月8日

@author: huawei
'''
from celery import Celery, Task

app = Celery()

class MyBaseTask(Task):
    abstract = True
    send_error_emails = True

app.Task = MyBaseTask
print app.Task

@app.task
def add(x, y):
    return x + y

print add

print add.__class__.mro()