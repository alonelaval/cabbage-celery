# -*- encoding: utf-8 -*-
'''
Created on 2016年6月17日

@author: hua
'''
from celery import events
from celery.app.base import Celery
from celery.events.state import Task



app = Celery('cabbage',backend="rpc://",broker='amqp://172.16.4.134')

if __name__=="__main__":
    print app.events.State().tasks_by_timestamp()
    tasks =  app.events.State().tasks_by_timestamp()
    for uuid, task in tasks:
        print uuid,task 
    print app.events.State().alive_workers()