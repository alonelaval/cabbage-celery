# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''

from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.log.logger import Logger
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.config import ConfigHolder
from cabbage.constants import JOBS, JOB_DELETE, CABBAGE, CONFIG, \
    BASE, WORKS, ON_LINE, LOST
from cabbage.data.store_holder import StoreHolder
from cabbage.event.server_jobs_event import \
    MonitorBrokerServerEvent, AddBrokerServerEvent
from cabbage.job.task_cache import TaskCacheHolder
import zope.event
log = Logger.getLogger(__name__)

kazooClient = ZookeeperClientHolder.getRetryClient()

#watch在第一次设置的时候就会运行一次
def testDataWatch(data, stat=None, event=None):
    print data
    print  stat
    print event
    

def updateJobCache(jobId):
    job=StoreHolder.getServerStore().getJob(jobId)
    CacheHolder.getCache().put(jobId, job,JOBS)

def workOnlineWatch(data, stat=None, event=None):
    if event is not None:
        #节点已死
        if event.type=="DELETED":
            #"/cabbage/works/"+HOST_NAME+"/"+ON_LINE
            hostName = event.path.split("/")[3]
            work =  StoreHolder.getServerStore().getWork(hostName)
            work.status = LOST
            Logger.info( log,"节点:【%s】IP:【%s】已经死亡！" % (hostName,work.ip) )
            StoreHolder.getServerStore().updateWorkStatus(work)
            
def workWatch(children):
    for hostname in children:
        if CacheHolder.getCache().hasKey(hostname, WORKS) is False:
            work =  StoreHolder.getServerStore().getWork(hostname)
            CacheHolder.getCache().put(hostname, work,WORKS)
            parent="/"+CABBAGE+"/"+WORKS+"/"+hostname
            kazooClient.addDataListener(parent+"/"+ON_LINE, workOnlineWatch)
            
            
def brokerServerWatch(children):
    for brokerName in children:
        if not CabbageHolder.getServerCabbages().has_key(brokerName):
            brokerServer = StoreHolder.getServerStore().getBrokerServer(brokerName)
            zope.event.notify(AddBrokerServerEvent(brokerServer))
            zope.event.notify(MonitorBrokerServerEvent(brokerServer))

#当监控的节点发生子节点变化时，将监控节点的所有的字节点已列表的方式返回,更新job缓存
def jobReadyWatch(children):
    try:
#         brokers={}
        for jobId in children:
            try:
                job=StoreHolder.getServerStore().getJob(jobId)
                if CacheHolder.getCache().hasKey(jobId, JOBS) is False:
                    CacheHolder.getCache().put(jobId, job,JOBS)
                    for taskName in job.tasks:
                        TaskCacheHolder.getJobCache().put(taskName,job.jobId)
            except Exception:
                Logger.exception( log)
            #偷个懒，只要没有删除的全部放到ROUTER里面去
#             if job.status != JOB_DELETE:
#                 
#                 for taskName in job.tasks:
#                     que=StoreHolder.getServerStore().getQueue(job.brokerQueue)
#                     TaskCacheHolder.getJobCache().put(taskName,job.jobId)
#                      
#                 if brokerServer in brokers:
#                     brokers[brokerServer].update(routes)
#                 else:
#                     brokers[brokerServer] = routes
#                 
#         #偷个懒，只要没有删除的全部放到ROUTER里面去
#         for broker,routes in brokers.items():
#             brokerServer = StoreHolder.getServerStore().getBrokerServer(broker)
#             CabbageHolder.getServerCabbages()[brokerServer.hostName].getApp().conf.update(CELERY_ROUTES = routes)
#             Logger.info(log,"更新队列服务器【%s】ROUTES【%s】"% (CabbageHolder.getServerCabbagesStr(),str(routes)))
        
    except Exception:
        Logger.exception( log)


# def jobWebWatch(children):
#     try:
#         brokers={}
#         for jobId in children:
#             job=StoreHolder.getStore().getJob(jobId)
#             if CacheHolder.getCache().hasKey(jobId, JOBS) is False:
#                 CacheHolder.getCache().put(jobId, job,JOBS)
#                 
#             #偷个懒，只要没有删除的全部放到ROUTER里面去
#             if job.status != JOB_DELETE:
#                 brokerServer=job.brokerServer
#                
#                 routes={}
#                 for taskName in job.tasks:
#                     que=StoreHolder.getStore().getQueue(job.brokerQueue)
#                     routes[taskName]={'queue': que.queueName, 'routing_key': que.routingKey}
#                     TaskCacheHolder.getJobCache().put(taskName,job.jobId)
#                      
#                 if brokerServer in brokers:
#                     brokers[brokerServer].update(routes)
#                 else:
#                     brokers[brokerServer] = routes
#                 
#         #偷个懒，只要没有删除的全部放到ROUTER里面去
#         for broker,routes in brokers.items():
#             brokerServer = StoreHolder.getStore().getBrokerServer(broker)
#             CabbageHolder.getServerCabbages()[brokerServer.hostName].getApp().conf.update(CELERY_ROUTES = routes)
#             Logger.info(log,"更新队列服务器【%s】ROUTES【%s】"% (CabbageHolder.getServerCabbagesStr(),str(routes)))
#         
#     except Exception:
#         Logger.exception( log)
        
CONFIG_PATH="/cabbage/config"
def configOptionDataChange(data, stat=None, event=None):
    if data and event is not None:
#         print data,stat,event
        # exmaple /cabbage/config/jobexecutorcount
        key = event.path.split("/")[2]
        ConfigHolder.getConfig().setProperty(BASE,key ,data)
        
    
def configWatch(children):
    try:
        for l in children :
            pa =CONFIG_PATH+"/"+l
            kazooClient.addDataListener(pa, configOptionDataChange)
            data= kazooClient.getData(pa)
            ConfigHolder.getConfig().setProperty(BASE,l ,data)
            
    except Exception:
        Logger.exception( log)
        

# kazooClient.addChildListener(CONFIG_PATH, configWatch)       
        
        
        

    