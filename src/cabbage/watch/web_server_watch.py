# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''

from cabbage.cabbage_celery.cabbage_for_celery import Cabbage
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.log.logger import Logger
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.config import ConfigHolder
from cabbage.constants import JOBS, JOB_DELETE, BASE, WORKS
from cabbage.data.store_factory import storeFactory
from cabbage.event.server_jobs_event import AddBrokerServerEvent
from cabbage.job.task_cache import TaskCacheHolder
import zope.event
log = Logger.getLogger(__name__)

#watch在第一次设置的时候就会运行一次
def testDataWatch(data, stat=None, event=None):
    print data
    print  stat
    print event
    

def updateJobCache(jobId):
    store = storeFactory.getStore()
    try:
        job=store.getJob(jobId)
        CacheHolder.getCache().put(jobId, job,JOBS)
    finally:
        storeFactory.returnStroe(store)
    
def workWatch(children):
    store = storeFactory.getStore()
    try:
        for hostname in children:
            if CacheHolder.getCache().hasKey(hostname, WORKS) is False:
                    work = store.getWork(hostname)
                    CacheHolder.getCache().put(hostname, work,WORKS)
    finally:
        storeFactory.returnStroe(store)

def brokerServerWatch(children):
    for brokerName in children:
        if not CabbageHolder.getServerCabbages().has_key(brokerName):
            store = storeFactory.getStore()
            try:
                brokerServer = store.getBrokerServer(brokerName)
                zope.event.notify(AddBrokerServerEvent(brokerServer))
            finally:
                storeFactory.returnStroe(store)

# kazooClient = ZookeeperClientHolder.getRetryClient()

def jobWebWatch(children):
    store = storeFactory.getStore()
    try:
        brokers={}
        for jobId in children:
            try:
                job=store.getJob(jobId)#toreHolder.getStore().getJob(jobId)
                if CacheHolder.getCache().hasKey(jobId, JOBS) is False:
                    CacheHolder.getCache().put(jobId, job,JOBS)
                
#                 kazooClient.addDataListener(parent+"/"+STATUS, jobRunStatusWatch)
                #偷个懒，只要没有删除的全部放到ROUTER里面去
                if job.status != JOB_DELETE:
                    brokerServer=job.brokerServer
                   
                    routes={}
                    for taskName in job.tasks:
                        que=store.getQueue(job.brokerQueue)
                        routes[taskName]={'queue': que.queueName, 'routing_key': que.routingKey}
                        TaskCacheHolder.getJobCache().put(taskName,job.jobId)
                         
                    if brokerServer in brokers:
                        brokers[brokerServer].update(routes)
                    else:
                        brokers[brokerServer] = routes
            except Exception:
                Logger.exception( log)
                
        #偷个懒，只要没有删除的全部放到ROUTER里面去
        for broker,routes in brokers.items():
            brokerServer = store.getBrokerServer(broker)
            #修复BUG，导致任务提交的celery队列里面去了
            cabbage = Cabbage(hostName=brokerServer.hostName,broker=brokerServer.connectUri)
            cabbage.app.conf.update(CELERY_ROUTES = routes)
            CabbageHolder.getServerCabbages()[brokerServer.hostName] = cabbage
            
#             CabbageHolder.getServerCabbages()[brokerServer.hostName].getApp().conf.update(CELERY_ROUTES = routes)
            Logger.info(log,"更新队列服务器【%s】ROUTES【%s】"% (brokerServer.hostName,str(routes)))
        
    except Exception:
        Logger.exception( log)
    finally:
        storeFactory.returnStroe(store)
        
CONFIG_PATH="/cabbage/config"
def configOptionDataChange(data, stat=None, event=None):
    if data and event is not None:
        print data,stat,event
        # example /cabbage/config/jobexecutorcount
        key = event.path.split("/")[2]
        ConfigHolder.getConfig().setProperty(BASE,key ,data)
        
def configWatch(children):
    kazooClient =  ZookeeperClientHolder.getRetryClient()
    try:
        for l in children :
            pa =CONFIG_PATH+"/"+l
            kazooClient.addDataListener(pa, configOptionDataChange)
            data= kazooClient.getData(pa)
            ConfigHolder.getConfig().setProperty(BASE,l ,data)
            
    except Exception:
        Logger.exception( log)
        
        

    