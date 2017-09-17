# -*- encoding: utf-8 -*-
'''
Created on 2017年7月15日

@author: huawei

import cabbage.test.celery4.add_task_test'''


from cabbage.test.celery4.myapp import app
from cabbage.utils.host_name import HOST_NAME
import sys
from celery.bin.worker import worker, main as worker_main
 
if __name__ == '__main__':
    print dir()

    print sys.path
    
    s, sys.argv = sys.argv, ['worker', '--discard']
    try:
        worker_main(app=app)
    finally:
        sys.argv = s
            
#     argv =['worker',
#                '--without-mingle',
#                '--without-gossip',
# #                '--without-heartbeat'
#                 '--autoscale=10,0'
#                ]
#     app.worker_main(argv)