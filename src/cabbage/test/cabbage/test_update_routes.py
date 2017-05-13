# -*- encoding: utf-8 -*-
'''
Created on 2016年11月17日

@author: huawei
'''
from celery.app.base import Celery

routes = {u'test_both_task.TestBothTask': {'queue': 'huawei', 'routing_key': 'huawei'}, u'test_ubuntu_task.TestUbuntuTask': {'queue': 'ubuntu', 'routing_key': 'ubuntu'}}

mac_routes = {u'test_mac_task.TestMacTask': {'queue': 'huawei', 'routing_key': 'huawei'}}


app = Celery('cabbage',broker='amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost')
app.config_from_object("cabbage.cabbage_celery.celeryconfig")
app.conf.update(CELERY_ROUTES=routes)


app.send_task("test_ubuntu_task.TestUbuntuTask",kwargs={"jobId":"job-a986d7d9-4950-4c45-a3c5-6553d81d5a36","no":2})

origRoutes = app.conf["CELERY_ROUTES"]
print app.tasks
print "CELERY_ROUTES:[%s]" % app.conf["CELERY_ROUTES"] 

origRoutes.update(mac_routes)
print origRoutes
print "-------------------------------------------------"

app.conf.update(CELERY_ROUTES=origRoutes)


app.send_task("test_mac_task.TestMacTask",kwargs={"jobId":"job-a986d7d9-4950-4c45-a3c5-6553d81d5a36","no":1})

print app.tasks
print "CELERY_ROUTES:[%s]" % app.conf["CELERY_ROUTES"] 

# origRoutes.update(mac_routes)
# print origRoutes

# 
#  
# CELERY_QUEUES = ( Queue('celery', Exchange('celery'), routing_key='celery'),)
# 
# 
# CELERY_ROUTES ={u'test_both_task.TestBothTask': {'queue': 'both', 'routing_key': 'both'}, u'test_both_task.TestBoth': {'queue': 'both', 'routing_key': 'both'}, u'test_mac_task.TestMacTask': {'queue': 'mac', 'routing_key': 'mac'}, u'test_ubuntu_task.TestUbuntuTask': {'queue': 'ubuntu', 'routing_key': 'ubuntu'}}
#  
# app.conf.update(CELERY_ROUTES=CELERY_ROUTES)
# 
# CELERY_QUEUES = ( Queue('default', Exchange('default'), routing_key='default'),
# )