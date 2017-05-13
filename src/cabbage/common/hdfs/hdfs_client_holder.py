# -*- encoding: utf-8 -*-
'''
Created on 2016年9月23日

@author: huawei
'''
from cabbage.common.hdfs.hdfs_client import HdfsClient
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, HDFS_URL


class HdfsClientHolder:
    @classmethod
    def getHdfsClient(cls):
        return HdfsClient(url=ConfigHolder.getConfig().getProperty(BASE,HDFS_URL))