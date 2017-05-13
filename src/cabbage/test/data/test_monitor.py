# -*- encoding: utf-8 -*-
'''
Created on 2016年9月13日

@author: huawei
'''


from cabbage.data.entity import TaskMonitor, JobMonitor, \
    DateMonitor, WorkMonitor, BrokerMonitor, Monitor
from cabbage.data.store_holder import StoreHolder
from unittest.case import TestCase
import unittest

        
        
class TestMonitor(TestCase):
    def test_save_Monitor(self):
        taskCount=2
        taskSucceeded=1
        taskFailed=1
        taskRuntime=1
        taskName="task-test"
        jobId="job-test"
        hour="1"
        date="20160913"
        hostName="test"
        brokerServer="test"
        taskQueueTime=1
        taskMonitor = TaskMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,taskName=taskName,jobId=jobId,taskQueueTime=taskQueueTime)
        jobMonitor = JobMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,jobId=jobId,taskMonitors=[taskMonitor],taskQueueTime=taskQueueTime)
        dateMonitor = DateMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,date=date,hour=hour)
        workMonitor = WorkMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,taskMonitors=[taskMonitor],dateMonitors=[dateMonitor],hostName=hostName)
        brokerMonitor=BrokerMonitor(taskCount=taskCount,taskSucceeded=taskSucceeded,taskFailed=taskFailed,taskRuntime=taskRuntime,brokerServer=brokerServer,taskQueueTime=taskQueueTime)
        
        monitor = Monitor(jobMonitors=[jobMonitor],workMonitors=[workMonitor],brokerMonitors=[brokerMonitor])
        
        StoreHolder.getServerStore().saveMonitor(monitor)
        
    def test_get_job(self):
        jobId="job-test"
        jobMonitor = StoreHolder.getServerStore().getJobMonitor(jobId)
        print jobMonitor.taskMonitors[0].taskName
        print jobMonitor.taskQueueTime
        
    def test_get_work(self):
        hostName="test"
        workMonitor = StoreHolder.getServerStore().getWorkMonitor(hostName)
        print workMonitor.taskMonitors[0].taskName
        print workMonitor.taskMonitors[0].taskQueueTime
        
    def test_get_broker(self):
        brokerServer="test"
        brokerMonitor=StoreHolder.getServerStore().getBrokerMonitor(brokerServer)
        print brokerMonitor.taskCount
        print brokerMonitor.taskQueueTime
        
        
if __name__=='__main__':
    unittest.main()