# -*- encoding: utf-8 -*-
'''
Created on 2016年9月20日

@author: huawei
'''
from cabbage.data.entity import WorkMonitor
aaa = WorkMonitor(hostName="aaa")


bbb = WorkMonitor(hostName="aaa")
aaa.taskMonitors.append(5)
bbb.taskMonitors.append(7)
print aaa.taskMonitors
print bbb.taskMonitors