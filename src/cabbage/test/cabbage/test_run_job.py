# -*- encoding: utf-8 -*-
'''
Created on 2016年9月9日

@author: huawei
'''
from cabbage.utils.date_util import getNowDateStr, getNow
import requests
import time
# jobId="job-7dce2427-2a23-4ab9-b033-5ca2a41cc001"
# test="job-da019109-6296-42ef-b8f5-4e8af4241349"
# test2="job-f1ec097f-9130-4e4e-abf1-30062cef438b"
# test3="job-3f451485-51ac-4912-abe6-786b8d710e87"


both ="job-29f3a426-267b-4fbd-97d8-919e693e030d"
mac="job-138d5bb7-8489-47a8-9b79-994aab068900"
ubuntu="job-6911124b-1f7c-4acc-a155-fb4513b74bc2"
# error="job-9103ee58-1368-4406-879a-463daa8d0d79"
# hdfs="job-00faa376-e9c1-4079-93b2-19bb3db57f4a"
# long_time="job-b81fc441-a1e6-40ef-ab6f-5400e61e6614"
# 
# nfs="job-57cebce9-8eff-4853-9ac4-e119cd8235f4"

url="http://127.0.0.1:2048/runJob"
# url ="http://101.198.156.26:2048/runJob"

begin=  getNow()
for i in range(10):
#     time.sleep(1)
    print i
#     requests.post(url, data = {'jobId':mac,"params":i})
    requests.post("http://127.0.0.1:2048/runJob", data = {'jobId':both})
    requests.post("http://127.0.0.1:2048/runJob", data = {'jobId':mac})
    requests.post("http://127.0.0.1:2048/runJob", data = {'jobId':ubuntu})
print "begin:【%s】 end:【%s】"%(begin,getNow())
