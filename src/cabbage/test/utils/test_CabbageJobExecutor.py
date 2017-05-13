# -*- encoding: utf-8 -*-
'''
Created on 2016年9月23日

@author: huawei
'''
# from cabbage.process.cabbage_job_excutor import \
#     CabbageJobExecutorHolder
# from cabbage.test.utils.test_CabbageJobExecutor import self
from cabbage.process.cabbage_job_excutor import \
    CabbageJobExecutorHolder
from concurrent import futures

def helloworld(jobId,aaa=None):
    print jobId
    
CabbageJobExecutorHolder.getCabbageJobExecutor().addAction(helloworld,123456,aaa=1)

# executor =  futures.ThreadPoolExecutor(max_workers=20)
# executor.submit(helloworld,123456)



# print 12121