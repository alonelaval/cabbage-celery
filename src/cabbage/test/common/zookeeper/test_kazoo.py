# -*- encoding: utf-8 -*-
'''
Created on 2016年6月3日

@author: hua
'''

from cabbage.common.zookeeper.kazoo_zookeeper_client import \
    KazooZookeeperClient
import unittest

class TestKazoo(unittest.TestCase):
#         self.kazooClient = KazooZookeeperClient("172.16.4.134:2181")

    def setUp(self):
        self.kazooClient = KazooZookeeperClient("172.16.4.134:2181")
#     def test_create(self):
#         if self.kazooClient.isExistPath("单独") is False:
#             self.kazooClient.delete("/单独", False)
#             self.kazooClient.create("/单独",value=u"打")
             
#     def test_create_child(self):
#         if self.kazooClient.isExistPath("/huawei/huawei2/huawei1") is False:
#             self.kazooClient.create("/huawei/huawei2/huawei1", False,value="son of bitch")
#     def test_putdata(self):
#         self.kazooClient.putData("huawei", "huawei")
#     def test_getdata(self):
#         print self.kazooClient.getData("huawei")
#     def test_get_child(self):
#         print self.kazooClient.getChildren("/huawei")
    def test_get_child_len(self):
        print len(self.kazooClient.getChildren("/cabbage/jobs/results"))
#         
#     def test_get_child_recursion(self):
#         for i in  self.kazooClient.getFullPathChildren("cabbage",  recursion=True):
#             print i
#     def test_create_cabbage(self):
#         if self.kazooClient.isExistPath("cabbage") is False:
#             self.kazooClient.create("cabbage", False)
#              
        
if __name__=="__main__":
    unittest.main()
