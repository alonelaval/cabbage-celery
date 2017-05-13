# -*- encoding: utf-8 -*-
'''
Created on 2016年9月22日

@author: huawei
'''
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.scheduler.scheduler_holder import \
    JobManageHolder
from cabbage.config import ConfigHolder
from cabbage.constants import JOBS, BASE, RESULTE_UPLOAD_SCHEDULER, \
    WORKS, OFF_LINE, ON_LINE
from cabbage.data.store_holder import StoreHolder
from cabbage.files.upload_job_result_file import doAction, \
    JobUploadPoolHolder
from cabbage.monitor.monitor_handlers import registerMoniters
from cabbage.monitor.monitor_stat_action import monitorJob
from concurrent import futures
# from cabbage.job.job_result_check import checkResult
# from cabbage.utils.date_util import getNowMinute, getNowHour

def serverScheduler():
    registerMoniters()
#     checkResultScheduler = "%s %s * * *"%(int(getNowMinute())+1,getNowHour()) 
    
#     JobManageHolder.getJobManage().addJob(checkResult,jobId="checkResult",cron="*/1 * * * *")
    
    JobManageHolder.getJobManage().addJob(monitorJob,jobId="monitor",cron="*/1 * * * *")
    
    resultUploadScheduler = ConfigHolder.getConfig().getProperty(BASE,RESULTE_UPLOAD_SCHEDULER)
    JobManageHolder.getJobManage().addJob(uploadServerScheduler,jobId="uploadServerScheduler",cron=resultUploadScheduler)
#     JobManageHolder.getJobManage().addJob(serverCheckWorkIsOffLine,jobId="serverCheckWorkIsOffLine",cron="0 * * * *")
    
def clientScheduler():
    resultUploadScheduler = ConfigHolder.getConfig().getProperty(BASE,RESULTE_UPLOAD_SCHEDULER)
    JobManageHolder.getJobManage().addJob(uploadClientScheduler,jobId="uploadClientScheduler",cron=resultUploadScheduler)
    

# def serverCheckWorkIsOffLine():
#     hostnames  = CacheHolder.getCache().getRegion(WORKS).namespace.keys()
# 
#     for hostname in hostnames:
#         work = CacheHolder.getCache().get(hostname,WORKS)
#         #FIXME 未分配的队列的节点 不用check
#         #TODO   
#         if work.brokerServer is None or work.brokerServer == '':
#             continue 
#         workIsAlive = CabbageHolder.getServerCabbage(work.brokerServer).workIsAlive(hostname)
#         if work.status == ON_LINE and not workIsAlive:
#             work.status = OFF_LINE
#             StoreHolder.getServerStore().updateWorkStatus(work)
#         
#         CacheHolder.getCache().put(hostname, work, WORKS)
    
# executor =  futures.ThreadPoolExecutor(max_workers=20)

def uploadServerScheduler():
    jobIds  = CacheHolder.getCache().getRegion(JOBS).namespace.keys()
    for jobId in jobIds:
#         executor.submit(doAction,jobId)
        JobUploadPoolHolder.getJobUploadPool().add(jobId)
        
def uploadClientScheduler():
    jobIds  = CacheHolder.getCache().getRegion(JOBS).namespace.keys()
    for jobId in jobIds:
#         executor.submit(doAction,jobId)
        JobUploadPoolHolder.getJobUploadPool().add(jobId)
        
