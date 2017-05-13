# -*- encoding: utf-8 -*-
'''
Created on 2016年11月18日

@author: huawei
'''

from kazoo.client import KazooClient
import time

zk = KazooClient(hosts="172.16.4.134:2181")
zk.start()

zk.create("/xj", "value1",ephemeral=True)

time.sleep(20)