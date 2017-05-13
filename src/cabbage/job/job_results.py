# -*- encoding: utf-8 -*-
'''
Created on 2016年9月21日

@author: huawei
'''
from cabbage.files.cabbage_path import getLocalFilesPath
from cabbage.utils.date_util import getNowDateStr, getNowHour
from concurrent import futures
import os
import threading

SIZE = 100
class JobResults(object):
    def __init__(self):
        self._results = {}
        self.executor =  futures.ThreadPoolExecutor(max_workers=5)
        self.lock =threading.Lock()
    
        
    def addResult(self,jobId,result):
#         try:
#             self.lock.acquire()
            
        localPath = getLocalFilesPath()
        dateStr = getNowDateStr()
        hour = str(getNowHour())
        resultDire=localPath+"/"+jobId+"/result"+"/"+dateStr
      
        if not os.path.isdir(resultDire):
            os.makedirs(resultDire)
        
        resultPath= resultDire+"/"+hour
        with open(resultPath,"a+") as writer:
            writer.write("%s \n" % result)
            
#             if jobId in self._results:
#                 datas = self._results[jobId] 
#                 datas.append(result)
#                 if len(datas) >= 100:#100行写到文件里面去
#                     self.executor.submit(self.saveResults,jobId)
#             else:
#                 datas = [result]
#                 self._results[jobId]= datas
            
#         finally:
#             self.lock.release()
    
#     def saveAllResults(self):
#         try:
#             self.lock.acquire()
#             for jobId in self._results.keys():
#                 datas = self._results[jobId] 
#                 localPath = getLocalFilesPath()
#                 dateStr = getNowDateStr()
#                 hour = str(getNowHour())
#                 resultDire=localPath+"/"+jobId+"/result"+"/"+dateStr
#                 resultPath= resultDire+"/"+hour
#                 if not os.path.isdir(resultDire):
#                     os.makedirs(resultDire)
#                 
#                 with open(resultPath,"a+") as writer:
#                     for data in datas :
#                         writer.write("%s \n" % data)
#             
#         finally:
#             self.lock.release()
#             
#             
#     def saveResults(self,jobId):
#         try:
#             self.lock.acquire()
#             datas = self._results[jobId] 
#             localPath = getLocalFilesPath()
#             dateStr = getNowDateStr()
#             hour = str(getNowHour())
#             resultDire=localPath+"/"+jobId+"/result"+"/"+dateStr
#             resultPath= resultDire+"/"+hour
#             if not os.path.isdir(resultDire):
#                 os.makedirs(resultDire)
#             
#             with open(resultPath,"a+") as writer:
#                 for data in datas :
#                     writer.write("%s \n" % data)
#             
#         finally:
#             self.lock.release()

jobResults = JobResults()
