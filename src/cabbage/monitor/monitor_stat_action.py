# -*- encoding: utf-8 -*-
'''
Created on 2016年9月14日

@author: huawei
'''
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.log.logger import Logger
from cabbage.constants import TASK_COUNT, TASK_RUNTIME, \
    TASK_QUEUE_TIME, TASK_SUCCEEDED, TASK_FAILED, TASKS, JOBS, TASK_RECEIVED
from cabbage.data.entity import TaskMonitor, JobMonitor, \
    WorkMonitor, DateMonitor, BrokerMonitor, Monitor
from cabbage.data.store_holder import StoreHolder
from cabbage.job.task_cache import TaskCacheHolder
from cabbage.monitor.cabbage_counter import CabbageCounterHolder
from cabbage.utils.date_util import getNowDateStr, getNowHour

log = Logger.getLogger(__name__)

'''
taskFail: {u'test_fail_task.TestFailTask': {u'huamac': 10}}

taskReceived: {u'test_both_task.TestBothTask': {u'huamac': 5, u'ubuntu': 5},
               u'test_fail_task.TestFailTask': {u'huamac': 10},
               u'test_mac_task.TestMacTask': {u'huamac': 10}}
             
taskSent: {u'test_both_task.TestBothTask': 10, 
            u'test_fail_task.TestFailTask': 10,
             u'test_mac_task.TestMacTask': 10}
             
taskSucceeded: {u'test_both_task.TestBothTask': {u'huamac': {'taskRuntime': 0.007029995998891536, 'taskCount': 5, 'taskQueueTime': 0.005977153778076172},
                                                 u'ubuntu': {'taskRuntime': 0.012823636003304273, 'taskCount': 5, 'taskQueueTime': 0.013159990310668945}},
                 u'test_mac_task.TestMacTask': {u'huamac': {'taskRuntime': 0.013582768006017432, 'taskCount': 10, 'taskQueueTime': 0.013071060180664062}}
                }

tasks: {u'test_both_task.TestBothTask': {'taskFailed': 0, 'taskRuntime': 0.17578555196496382, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.05704784393310547}, u'test_fail_task.TestFailTask': {'taskFailed': 10, 'taskRuntime': 0, 'taskSucceeded': 0, 'taskCount': 10, 'taskQueueTime': 0}, u'test_mac_task.TestMacTask': {'taskFailed': 0, 'taskRuntime': 0.013801397988572717, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.012968063354492188}}
works: {u'huamac': {'taskRuntime': 0.02174860195373185, 'taskSucceeded': 15, 'taskCount': 25, 'taskFailed': 10}, u'ubuntu': {'taskRuntime': 0.16783834799980468, 'taskSucceeded': 5, 'taskCount': 5}}
workTasks: {u'huamac': {u'test_both_task.TestBothTask': {'taskRuntime': 0.007947203965159133, 'taskSucceAAeded': 5, 'taskCount': 5, 'taskQueueTime': 0.008563041687011719}, u'test_fail_task.TestFailTask': {'taskCount': 10, 'taskFailed': 10}, u'test_mac_task.TestMacTask': {'taskRuntime': 0.013801397988572717, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.012968063354492188}}, u'ubuntu': {u'test_both_task.TestBothTask': {'taskRuntime': 0.16783834799980468, 'taskSucceeded': 5, 'taskCount': 5, 'taskQueueTime': 0.04848480224609375}}} 


jobs: {u'job-f464b77b-f3f0-4ef4-9442-0bb1817d00dc': {'tasks': set([u'test_mac_task.TestMacTask']), 'taskQueueTime': 0.014971733093261719, 'taskRuntime': 0.013479260000167415, 'taskCount': 10, 'taskFailed': 0, 'taskSucceeded': 10}, u'job-abd79498-883f-4569-bf1f-e09d48c45ffc': {'tasks': set([u'test_fail_task.TestFailTask']), 'taskQueueTime': 0, 'taskRuntime': 0, 'taskCount': 10, 'taskFailed': 10, 'taskSucceeded': 0}, u'job-2984c37a-86fe-44cd-8e4d-dc18affa8476': {'tasks': set([u'test_both_task.TestBothTask']), 'taskQueueTime': 0.03728485107421875, 'taskRuntime': 0.06659536307051894, 'taskCount': 10, 'taskFailed': 0, 'taskSucceeded': 10}} 
brokers: {'cabbage': {'taskQueueTime': 0.05225658416748047, 'taskRuntime': 0.08007462307068636, 'taskSucceeded': 20, 'taskCount': 30, 'taskFailed': 10}}
tasks: {u'test_both_task.TestBothTask': {'taskFailed': 0, 'taskRuntime': 0.06659536307051894, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.03728485107421875}, u'test_fail_task.TestFailTask': {'taskFailed': 10, 'taskRuntime': 0, 'taskSucceeded': 0, 'taskCount': 10, 'taskQueueTime': 0}, u'test_mac_task.TestMacTask': {'taskFailed': 0, 'taskRuntime': 0.013479260000167415, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.014971733093261719}}
works: {u'huamac': {'taskRuntime': 0.02175475106923841, 'taskSucceeded': 15, 'taskCount': 25, 'taskFailed': 10}, u'ubuntu': {'taskRuntime': 0.05831987200144795, 'taskSucceeded': 5, 'taskCount': 5}}
workTasks: {u'huamac': {u'test_both_task.TestBothTask': {'taskRuntime': 0.008275491069070995, 'taskSucceeded': 5, 'taskCount': 5, 'taskQueueTime': 0.008256673812866211}, u'test_fail_task.TestFailTask': {'taskCount': 10, 'taskFailed': 10}, u'test_mac_task.TestMacTask': {'taskRuntime': 0.013479260000167415, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.014971733093261719}}, u'ubuntu': {u'test_both_task.TestBothTask': {'taskRuntime': 0.05831987200144795, 'taskSucceeded': 5, 'taskCount': 5, 'taskQueueTime': 0.02902817726135254}}} 

        
taskMonitor = TaskMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,taskName=taskName,jobId=jobId,taskQueueTime=taskQueueTime)
jobMonitor = JobMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,jobId=jobId,taskMonitors=[taskMonitor],taskQueueTime=taskQueueTime)
dateMonitor = DateMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,date=date,hour=hour)
workMonitor = WorkMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,taskMonitors=[taskMonitor],dateMonitors=[dateMonitor],hostName=hostName)
brokerMonitor=BrokerMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,brokerServer=brokerServer,taskQueueTime=taskQueueTime)
        
monitor = Monitor(jobMonitors=[jobMonitor],workMonitors=[workMonitor],brokerMonitors=[brokerMonitor])
'''
#badcode
def _setValue(obj,key,value):
    if  hasattr(obj,key):
        origValue = getattr(obj,key)
        if origValue is None or origValue == 'None':
            origValue = 0
        else:
            origValue = float(origValue)
        if value is None:
            value = 0    
        newValue = origValue+value
        setattr(obj,key,newValue)
    
def statAciton(taskSentDict,taskReceivedDict,taskFailDict,taskSucceededDict):
    log.info("开始统计系统TASK运行情况 !")

    tasks={}  
    works={}
    workTasks={}
#     taskSucceeded = 0
#     taskRuntime=0
#     taskQueueTime =0
#     taskFailed=0
    for taskName,value in taskSentDict.items():
        taskCount = value
        tasks.update({taskName:{TASK_COUNT:taskCount,TASK_FAILED:0,TASK_SUCCEEDED:0,TASK_RUNTIME:0,TASK_QUEUE_TIME:0}})
    
    for taskName,taskValues in taskFailDict.items():
        taskFailed = 0
        for work,value in taskValues.items():
            taskFailedTemp  = value
            if work in workTasks:
                if taskName in workTasks[work]:
                    workTasks[work][taskName][TASK_FAILED]=taskFailedTemp
                else:
                    workTasks[work].update({taskName:{TASK_FAILED:taskFailedTemp}})
            else:
                workTasks[work]={taskName:{TASK_FAILED:taskFailedTemp}}
                
            if work in works:
                if TASK_FAILED in works[work]: 
                    works[work][TASK_FAILED] = works[work][TASK_FAILED]+taskFailedTemp
                else:
                    works[work].update({TASK_FAILED:taskFailedTemp})
            else:
                works[work]={TASK_FAILED:taskFailedTemp}
            
            taskFailed+= taskFailedTemp
        
        if taskName in tasks:
            tasks[taskName].update({TASK_FAILED:taskFailed})
        else:
            tasks.update({taskName:{TASK_FAILED:taskFailed}})
            
#     print tasks 
#     print taskSucceededDict
    for taskName,taskValues in taskSucceededDict.items():
        taskSucceeded = 0
        taskRuntime=0
        taskQueueTime =0
        for work,value in taskValues.items():
            taskSucceededTemp =  value[TASK_COUNT]
            taskRuntimeTemp = value[TASK_RUNTIME]
            taskQueueTimeTemp =value[TASK_QUEUE_TIME]
            
            if work in workTasks:
                    workTasks[work].update({taskName:{TASK_SUCCEEDED:taskSucceededTemp,TASK_RUNTIME:taskRuntimeTemp,TASK_QUEUE_TIME:taskQueueTimeTemp}})
            else:
                workTasks[work]={taskName:{TASK_SUCCEEDED:taskSucceededTemp,TASK_RUNTIME:taskRuntimeTemp,TASK_QUEUE_TIME:taskQueueTimeTemp}}
            
            
            if work in works:
                tempWork=works[work]
                if TASK_SUCCEEDED in tempWork:
                    tempWork[TASK_SUCCEEDED]= tempWork[TASK_SUCCEEDED]+taskSucceededTemp
                    tempWork[TASK_RUNTIME]= tempWork[TASK_RUNTIME]+taskRuntimeTemp
                else:
                    tempWork.update({TASK_SUCCEEDED:taskSucceededTemp,TASK_RUNTIME:taskRuntimeTemp})
            else:
                works[work] = {TASK_SUCCEEDED:taskSucceededTemp,TASK_RUNTIME:taskRuntimeTemp}
                
            taskSucceeded +=  taskSucceededTemp
            taskRuntime += taskRuntimeTemp
            taskQueueTime += taskQueueTimeTemp
        
        if taskName in tasks:
            tasks[taskName].update({TASK_SUCCEEDED:taskSucceeded,TASK_RUNTIME:taskRuntime,TASK_QUEUE_TIME:taskQueueTime})
        else:
            tasks[taskName]={TASK_SUCCEEDED:taskSucceeded,TASK_RUNTIME:taskRuntime,TASK_QUEUE_TIME:taskQueueTime}
            
#     print tasks
    
    for taskName,value in taskReceivedDict.items():
        taskAllReceived=0
        for work,taskCountTemp in value.items():
            taskAllReceived += taskCountTemp
            if work in workTasks:
                if taskName in workTasks[work]:
                    workTasks[work][taskName][TASK_COUNT]=taskCountTemp
                else:
                    workTasks[work].update({taskName:{TASK_COUNT:taskCountTemp}})
            else:
                workTasks[work]={taskName:{TASK_COUNT:taskCountTemp}}
                        
            if work in works:
                if TASK_COUNT in works[work]: 
                        works[work][TASK_COUNT] = works[work][TASK_COUNT]+taskCountTemp
                else:
                    works[work].update({TASK_COUNT:taskCountTemp})
            else:
                works[work]={TASK_COUNT:taskCountTemp}
            
        if taskName in tasks:
            tasks[taskName].update({TASK_RECEIVED:taskAllReceived})
        else:
            tasks.update({taskName:{TASK_RECEIVED:taskAllReceived}})
            
            
     
#     print tasks
    #stat job
    jobs={}
    brokers={}
    taskMonitors={}
    for taskName,values in tasks.items():
        jobId = TaskCacheHolder.getJobCache().get(taskName)
        job = CacheHolder.getCache().get(jobId,JOBS)
        broker =job.brokerServer
        for key,value in values.items():
            if job.brokerServer in brokers:
                if key in brokers[broker]:
                    brokers[broker][key] = brokers[broker][key] + value
                else:
                    brokers[broker][key]= value
            else:
                brokers[broker]={key:value}
                
            if jobId in jobs:
                if key in jobs[jobId]:
                    jobs[jobId][key] = jobs[jobId][key] + value
                else:
                    jobs[jobId][key]= value
            else:
                jobs[jobId]={key:value}
                a = set()
                a.add(taskName)
                jobs[jobId][TASKS] = a
        
        jobs[jobId][TASKS].add(taskName)  
        
        taskMonitors[taskName] =TaskMonitor(taskCount=values[TASK_COUNT] if TASK_COUNT in values else 0,
                                            taskSucceeded=values[TASK_SUCCEEDED] if TASK_SUCCEEDED in values else 0,
                                            taskFailed=values[TASK_FAILED] if TASK_FAILED in values else 0,
                                            taskRuntime=values[TASK_RUNTIME] if TASK_RUNTIME in values else 0,
                                            taskName=taskName,jobId=TaskCacheHolder.getJobCache().get(taskName),
                                            taskQueueTime= values[TASK_QUEUE_TIME] if TASK_QUEUE_TIME in values else 0,
                                            taskReceived = values[TASK_RECEIVED] if TASK_RECEIVED in values else 0)
    
#     print jobs 
    jobMonitors=[]
#     print "taskMonitors: %s "%taskMonitors
    for jobId,values in jobs.items():
        jobMonitor = StoreHolder.getServerStore().getJobMonitor(jobId)
        if jobMonitor is None:
            jobMonitor=JobMonitor(jobId=jobId,taskMonitors=[])
            
        for key,value in values.items():
            #jobMonitor
            _setValue(jobMonitor,key,value)
        #taskMonitor
        for  taskName in values[TASKS]:
            taskMonitorTemp = taskMonitors[taskName]
            taskMonitor = None
            for taskMonitor in  jobMonitor.taskMonitors:
                if taskMonitor.taskName == taskName:
                    taskMonitor = taskMonitor
                    break 
            if taskMonitor:
                _setValue(taskMonitor,TASK_COUNT,taskMonitorTemp.taskCount)
                _setValue(taskMonitor,TASK_RECEIVED,taskMonitorTemp.taskReceived)
                _setValue(taskMonitor,TASK_SUCCEEDED,taskMonitorTemp.taskSucceeded)
                _setValue(taskMonitor,TASK_FAILED,taskMonitorTemp.taskFailed)
                _setValue(taskMonitor,TASK_RUNTIME,taskMonitorTemp.taskRuntime)
                _setValue(taskMonitor,TASK_QUEUE_TIME,taskMonitorTemp.taskQueueTime)
            else:
                jobMonitor.taskMonitors.append(taskMonitorTemp)
                    
        jobMonitors.append(jobMonitor)
        
    
    workMonitors = []
    
    dateStr = getNowDateStr()
    hour = str(getNowHour())
    
    for hostName,values in works.items():
        workMonitor = StoreHolder.getServerStore().getWorkMonitor(hostName)
        if  workMonitor is None:
            workMonitor = WorkMonitor(hostName=hostName,taskMonitors=[],dateMonitors=[])
      
        dateMonitor = StoreHolder.getServerStore().getWorkHourMonitor(hostName, dateStr, hour)
        if not dateMonitor:
            dateMonitor = DateMonitor(date=dateStr,hour=hour)
        
        for key,value in values.items():
            
            #workMonitor
            _setValue(workMonitor,key,value)
            #dateMonitor
            _setValue(dateMonitor,key,value)
            print key,value
        workMonitor.dateMonitors.append(dateMonitor)
        #taskMonitor
        wTasks =workTasks[hostName]
#         print id(workMonitor)
#         print wTasks
       
        for taskName,wvalues in wTasks.items():
            wTaskMonitor = None
            for tm in  workMonitor.taskMonitors:
                if tm.taskName == taskName:
                    wTaskMonitor = tm
                    break 
            if wTaskMonitor is None:
                wTaskMonitor = TaskMonitor(taskName=taskName)
                workMonitor.taskMonitors.append(wTaskMonitor) 
                
            for key,value in wvalues.items():
                _setValue(wTaskMonitor,key,value)
                    
        workMonitors.append(workMonitor)
    
    brokerMonitors = []
    for brokerName,values in brokers.items():
        brokerMonitor = StoreHolder.getServerStore().getBrokerMonitor(brokerName)
        if not  brokerMonitor :
            brokerMonitor = BrokerMonitor(brokerServer=brokerName)
        
        dateMonitor = StoreHolder.getServerStore().getBrokerDateMonitor(brokerName, dateStr)
        if dateMonitor is None:
            dateMonitor = DateMonitor(date=dateStr)
            
        for key,value in values.items():
            _setValue(brokerMonitor,key,value)
            _setValue(dateMonitor,key,value)
       
        
        brokerMonitor.dateMonitors.append(dateMonitor)
        
        brokerMonitors.append(brokerMonitor)
        
#     print "jobMonitors: %s "%jobMonitors
#     print "jobs: %s " % jobs
#     print "brokers: %s" % brokers
#     print "tasks: %s" % tasks 
#     print "works: %s" % works
#     print "workTasks: %s "%workTasks
# #         
#     print "taskFail: %s"%taskFailDict
#     print "taskReceived: %s"%taskReceivedDict
#     print "taskSent: %s"%taskSentDict
#     print "taskSucceeded: %s"%taskSucceededDict
        
    log.info("结束统计系统TASK运行情况 !")
    if len(jobMonitors) >0 or len(workMonitors) > 0 or len(brokerMonitors) > 0: 
        monitor = Monitor(jobMonitors=jobMonitors,workMonitors=workMonitors,brokerMonitors=brokerMonitors)
        StoreHolder.getServerStore().saveMonitor(monitor)
#         taskSentDict.clear()
#         taskReceivedDict.clear()
#         taskFailDict.clear()
#         taskSucceededDict.clear()
        
    
    
def monitorJob():
    CabbageCounterHolder.getCabbageCounter().doAction(statAciton)

