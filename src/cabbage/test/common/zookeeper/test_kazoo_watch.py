# -*- encoding: utf-8 -*-
'''
Created on 2016年6月13日

@author: hua
'''
from kazoo.client import KazooClient
import time

zk = KazooClient(hosts="172.16.4.134:2181")
zk.start()

@zk.DataWatch("/xj")
def changed(data, stat, event):
    print "--------------DataWatch---------------"
    print "data:", data
    print "stat:", stat
    print "event:", event

# zk.create("/xj", "value1")
# time.sleep(10)
# zk.set("/xj", "value2")
time.sleep(60)
# zk.delete("/xj")
# time.sleep(2)