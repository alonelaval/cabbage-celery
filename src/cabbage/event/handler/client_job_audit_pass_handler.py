# -*- encoding: utf-8 -*-
'''
Created on 2016年6月17日

@author: hua
'''
# from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
# from cabbage.common.cabbage.util import isCabbageTask
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.file.load_file_holder import LoadMoudleHolder
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import JOBS, BASE, CLIENT_FILE_DIRECTORY, \
    PYTHON, DONE
from cabbage.data.store_factory import storeFactory
from cabbage.event.client_jobs_event import JobNeedLoadEvent
from cabbage.message.file_message import FileRequestMessage
from cabbage.net.client import SocketClient
# from cabbage.process.cabbage_control_holder import \
#     CabbageControlHolder
from cabbage.utils.host_name import HOST_NAME
import time
import zope.event
# from cabbage.data.store_holder import StoreHolder
log = Logger.getLogger(__name__)

def jobAuditPassHandler(event):
    try:
        jobId = event.jobId
        syncJob(jobId)
        #通知子进程进行加载模块
#         zope.event.notify(JobNeedLoadEvent(jobId))
        from cabbage.process.cabbage_control_holder import CabbageControlHolder
#         CabbageControlHolder.getCabbageControl().addJobId(event.jobId)
        CabbageControlHolder.getCabbageControl().restartCelery()
        
    except Exception:
        Logger.exception(log)
    
def syncJob(jobId,store=None):
    jobId = jobId
    if store is None:
        with storeFactory.store() as store:
            work=store.getWork(HOST_NAME)
            store.removeJobWorkReady(jobId, work)
    else:
        work=store.getWork(HOST_NAME)
        store.removeJobWorkReady(jobId, work)
    
    job = CacheHolder.getCache().get(jobId, JOBS)
    fileNames=[]
    #不同步主节点文件
#     CacheHolder.getCache().put(job.fileName, "", jobId)
#     try:
#         syncFile(job.fileName,jobId,FileRequestMessage.MAIN)
#     except Exception:
#         syncFile(job.fileName,jobId,FileRequestMessage.MAIN)
#          
#     fileNames.append(job.fileName)
    
    if job.attachFiles:
        for attachFile in job.attachFiles:
            CacheHolder.getCache().put(attachFile.fileName, "", jobId)
            try:
                syncFile(attachFile.fileName,jobId,FileRequestMessage.ATTACH)
            except Exception:
                syncFile(attachFile.fileName,jobId,FileRequestMessage.ATTACH)
            
            fileNames.append(attachFile.fileName)
            
    checkAllFileIsReady(fileNames,jobId)

def syncFile(fileName,jobId,tp):
    client = SocketClient()
    client.connect()
    requestMessage = FileRequestMessage()
    requestMessage.fileName =fileName
    requestMessage.jobId = jobId
    requestMessage.type = tp
    client.sendall(requestMessage)
    
    
def checkAllFileIsReady(fileNames,jobId,num=0):
    if num > 10:
        return
    
    for fileName in fileNames:
        value = CacheHolder.getCache().get(fileName, jobId)
        if value != DONE:
            time.sleep(10)
            checkAllFileIsReady(fileNames,jobId,num+1)
