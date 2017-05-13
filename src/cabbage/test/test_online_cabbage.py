# -*- encoding: utf-8 -*-
'''
Created on 2016年8月10日

@author: hua
'''
from celery.app.base import Celery


server ="amqp://cabbage_celery:cabbage_celery@123.59.211.146:5672/cabbage_vhost"
# server ="amqp://cabbage_celery_url:cabbage_celery_url@123.59.211.146:5672/cabbage_vhost_url"
# server="amqp://cabbage_celery:cabbage_celery@10.0.137.88:5672/cabbage_vhost"
# server="amqp://cabbage_celery:cabbage_celery@192.168.109.38:5672/cabbage_vhost"

# server="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost"

app = Celery('cabbage@huamac',backend="rpc://",broker=server)


# print "start job"
inspect = app.control.inspect()

av = inspect.active()
print av
print "---------------------------------------------"
result = inspect.stats()
print inspect.conf()
print "---------------------------------------------"
for key,v in  inspect.active_queues().items():
    queue_names = [i['name'] for i in v ]
    print key,queue_names
#     
print "---------------------------------------------"
# print len(result)
for key,v in result.items():
    print key,v
# print i.registered_tasks().keys
registeredTasks =inspect.registered_tasks()
print "---------------------------------------------"
print len(registeredTasks.items())
print "----------------------"
keys=  registeredTasks.keys()
#celery@UTN-C-100.qihoo.net
# ids = [ int(key.split('-')[2].split(".")[0]) for key in keys ]
# ids.sort()
# for i in ids:
#     print i
    
    
for key,v in registeredTasks.items():
    print key,v



