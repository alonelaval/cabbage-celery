# -*- encoding: utf-8 -*-
'''
Created on 2016年9月21日

@author: huawei
'''
from cabbage.common.hdfs.hdfs_client import HdfsClient
from unittest.case import TestCase
import os
import unittest
print __file__
class TestHDFS(TestCase):
    def test_request(self):
        client =HdfsClient()
        print client.isDirectory("/user")
        print client.isFile("/user/cabbage/install.sh")
        print client.ls("/user")
        client.get("/user/cabbage/install.sh", "/Users/hua/workspace/python/cabbage/src/com/pingansec/cabbage/test/common/hdfs/install.sh")
        client.get("/user/cabbage/test.txt", "/Users/hua/workspace/python/cabbage/src/com/pingansec/cabbage/test/common/hdfs/text.sh")
        client.mkdir("/user/cabbage/huawei")
        client.upload("/Users/hua/workspace/python/cabbage/src/com/pingansec/cabbage/test/common/hdfs/text.sh", "/user/cabbage/huawei/test.sh")
        client.dowload("/user/cabbage/huawei/test.sh", "/Users/hua/workspace/python/cabbage/src/com/pingansec/cabbage/test/common/hdfs/t1")
        
        
#         client.put( "/Users/hua/workspace/python/cabbage/src/com/pingansec/cabbage/test/common/hdfs/test.txt", "/user/cabbage/test.txt")
        
#         pass
            
    def test_respone(self):
        print os.listdir("/Users/hua/workspace/python/cabbage/src/com/pingansec/cabbage/test/common/hdfs")
        pass
    
if __name__=="__main__":
    unittest.main()
