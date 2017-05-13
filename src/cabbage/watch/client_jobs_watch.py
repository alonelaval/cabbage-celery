# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.log.logger import Logger
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
# from cabbage.config import ConfigHolder
from cabbage.constants import JOBS, CABBAGE, AUDIT_STATUS, STATUS, \
    JOB_AUTH_PASS, BROKER_SERVER, WORKS, QUEUES, DO_NOTHING, BASE, CONFIG
from cabbage.data.store_factory import storeFactory
from cabbage.data.store_holder import StoreHolder
from cabbage.event.client_jobs_event import JobAuditPassEvent, \
    JobStatusChangeEvent, WorkBrokerQueueChangeEvent, WorkBrokerServerChangeEvent, \
    ClientWorkStatusEvent
from cabbage.utils.host_name import HOST_NAME
import zope.event

kazooClient = ZookeeperClientHolder.getRetryClient()
CONFIG_PATH="/cabbage/config"

# import time
log = Logger.getLogger(__name__)

#watch在第一次设置的时候就会运行一次

def testDataWatch(data, stat=None, event=None):
    print data
    print  stat
    print event

def updateJobCache(jobId,job):
    CacheHolder.getCache().put(jobId, job, JOBS)

def updateWorkCache(hostName):
    with storeFactory.store() as store:
        work = store.getWork(hostName)
        CacheHolder.getCache().put(hostName,work,WORKS)
    
#当监控的节点发生子节点变化时，将监控节点的所有的字节点已列表的方式返回，
#只对我关注的job进行观察 
def jobChildWatch(children):
    try:
        for jobId in children:
            jobId = str(jobId)
            with storeFactory.store() as store:
                job=store.getJob(jobId)
                work = store.getWork(HOST_NAME)
            if CacheHolder.getCache().hasKey(jobId, JOBS) is False and job.brokerQueue in work.queues:
                '''添加job的状态监控'''
                parent="/"+CABBAGE+"/"+JOBS+"/"+jobId
                kazooClient.addDataListener(parent+"/"+STATUS, jobRunStatusWatch)
                kazooClient.addDataListener(parent+"/"+AUDIT_STATUS, jobAduitStatusWatch)
                updateJobCache(jobId,job)
    except Exception:
        Logger.exception( log)
#         traceback.print_exc()

#对该节点create、set、delete操作都会触发该watch
#data是该节点的值；stat是节点的ZnodeState状态信息；event是WatchedEvent类实例，有三个值：type表示触发该watch的操作类型（如CREATED表示是一个创建节点的操作触发了该watch）
#、state表示当前连接状态、path表示操作的路径。这三个参数也不是必须提供，提供一个或两个也行
#所有客户端监控JOBS目录，发现有新的job，对新建的job建立监控

#job审核通过后，客户端主动从服务器同步job所有的文件信息到客户端
def jobAduitStatusWatch(data,stat,event=None):
    try:
        if data and data == JOB_AUTH_PASS and event is not None:
            # example /cabbage/jobs/job-47778319-7a86-4b2b-a43a-5e2e94504350/status
            jobId = event.path.split("/")[3]
            with storeFactory.store() as store:
                job=store.getJob(jobId)
            updateJobCache(jobId,job)
            zope.event.notify(JobAuditPassEvent(jobId))
    except Exception:
        Logger.exception( log)
#         traceback.print_exc()

#job运行状态监控，如停止，暂停，运行，重启的操作
def jobRunStatusWatch(data,stat,event=None):
    try:
        if data and event is not None:
            jobId = event.path.split("/")[3]
            zope.event.notify(JobStatusChangeEvent(jobId))
    except Exception:
        Logger.exception( log)


def workStatusWatch(data,stat,event=None):
    try:
        if data and event is not None:
            #path=u'/cabbage/works/huamac/status')
            hostname= event.path.split("/")[3]
            if hostname == HOST_NAME:
                zope.event.notify(ClientWorkStatusEvent(data))
    except Exception:
        Logger.exception( log)
        

# @DeprecationWarning
# def worksWatch(children):
#     try:
#         for work in children:
#             work = str(work)
#             hostName = getHostName()
#             if work == hostName and CacheHolder.getCache().hasKey(hostName, WORKS) is False:
#                 updateWorkCache(hostName)
#                 parent="/"+CABBAGE+"/"+WORKS+"/"+hostName
#                 kazooClient.addDataListener(parent+"/"+BROKER_SERVER, workBrokerServerWatch)
#                 kazooClient.addChildListener(parent+"/"+QUEUES, workBrokerQueueWatch)
#     except Exception:
#         Logger.exception( log)
        

def workBrokerQueueWatch(children):
    try:
        data = kazooClient.getData("/"+CABBAGE+"/"+WORKS+"/"+HOST_NAME+"/"+QUEUES)
#         print data
        if data and data == DO_NOTHING:
            return
        zope.event.notify(WorkBrokerQueueChangeEvent(children,isEvent=True))
    except Exception:
        Logger.exception( log)

# @DeprecationWarning
# def workBrokerServerWatch(data,stat,event=None):
#     try:
#         if data and event is not None:
#             zope.event.notify(WorkBrokerServerChangeEvent(data,isEvent= event is not None))
#     except Exception:
#         Logger.exception( log)


    
# def configOptionDataChange(data, stat=None, event=None):
#     
#     if data and event is not None:
#         print data,stat,event
#         # exmaple /cabbage/config/jobexecutorcount
#         key = event.path.split("/")[2]
#         ConfigHolder.getConfig().setProperty(BASE,key ,data)
#         
#     
# def configWatch(children):
#     try:
#         for l in children :
#             pa ="/"+CABBAGE+"/"+CONFIG+"/"+l
#             kazooClient.addDataListener(pa, configOptionDataChange)
#             data= kazooClient.getData(pa)
#             ConfigHolder.getConfig().setProperty(BASE,l ,data)
#             
#     except Exception:
#         Logger.exception( log)
        
        
# kazooClient.addChildListener(CONFIG_PATH, configWatch)
    