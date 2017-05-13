# -*- encoding: utf-8 -*-
'''
Created on 2016年9月21日

@author: huawei
'''
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, UPLOAD_HDFS_FILE_PROCESS_COUNT, \
    NFS, HDFS, JOBS
from cabbage.data.store_factory import storeFactory
from cabbage.files.cabbage_hdfs_backend import CabbageHdfsBackend
from cabbage.files.cabbage_nfs_backend import CabbageNfsBackend
from cabbage.utils.util import singleton
from concurrent import futures
import Queue
import multiprocessing
# from cabbage.data.store_holder import StoreHolder

log=Logger.getLogger(__name__)

def action(queue):
        while True:
            try:
                jobId = queue.get()
                doAction(jobId)
            except Exception:
                Logger.exception(log)
                
def doAction(jobId):
    if not CacheHolder.getCache().hasKey(jobId, JOBS):
        with storeFactory.store() as store:
            job = store.getJob(jobId)
            CacheHolder.getCache().put(jobId,job,JOBS)
   
    job = CacheHolder.getCache().get(jobId,JOBS)
    
    Logger.debug( log, "upload files. job【%s】" % str(job.asDict()))
    
    if job.resultBackend == None:
        return 
    elif job.resultBackend == NFS:
        CabbageNfsBackend(jobId).save()
    elif job.resultBackend == HDFS:
        CabbageHdfsBackend(jobId).save()
    
@singleton
class JobProcessUploadPool():
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.jobIdQueue =self.manager.Queue()
        self.start()
    def add(self,jobId):
        self.jobIdQueue.put(jobId)
        
    def start(self):
        jobProcessCount = ConfigHolder.getConfig().getProperty(BASE,UPLOAD_HDFS_FILE_PROCESS_COUNT)
        self.pool = multiprocessing.Pool(processes =int(jobProcessCount))
        for i in range(int(jobProcessCount)):
            self.pool.apply_async(action,(self.jobIdQueue,))
            
@singleton
class JobThreadUploadPool():
    def __init__(self):
        self.max=ConfigHolder.getConfig().getProperty(BASE,UPLOAD_HDFS_FILE_PROCESS_COUNT)
        self.executor =  futures.ThreadPoolExecutor(max_workers=self.max)
        self.jobIdQueue = Queue.Queue()
        self.start()
    
    def add(self,jobId):
        self.jobIdQueue.put(jobId)
        
    def start(self):
        for i in range(int(self.max)):
            self.executor.submit(action,self.jobIdQueue)
    
class JobUploadPoolHolder():
    @classmethod 
    def getJobUploadPool(cls):
        return JobThreadUploadPool()
    
    