# -*- encoding: utf-8 -*-
'''
Created on 2016年8月26日

@author: huawei
'''
from celery.app.base import Celery
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
import collections
import time

appCelery = Celery('cabbage',backend="rpc://",broker='amqp://cabbage_celery:cabbage_celery@10.0.137.88:5672/cabbage_vhost')


INSPECT_METHODS = ('stats', 'active_queues', 'registered', 'scheduled',
                       'active', 'reserved', 'revoked', 'conf')
worker_cache = collections.defaultdict(dict)
pool = ThreadPoolExecutor(4)


def update_workers(app, workername=None):
    futures = []
    destination = None
#     timeout = app.inspect_timeout / 1000.0
    inspect = app.control.inspect()
    for method in INSPECT_METHODS:
        print getattr(inspect, method)()
#         futures.append(pool.submit(partial(getattr(inspect, method)))

#         futures.append(partial(getattr(inspect, method)))
#     results = yield futures
#     for i, result in enumerate(futures):
#         if result is None:
#             print "'%s' inspect method failed"% INSPECT_METHODS[i]
#             continue
#         for worker, response in result.items():
#             if response is not None:
#                 info = worker_cache[worker]
#                 info[INSPECT_METHODS[i]] = response
#                 info['timestamp'] = time
    

            
if __name__=="__main__":
    update_workers(appCelery)
#     for a in update_workers(appCelery):
#         print a
    
    print worker_cache
        