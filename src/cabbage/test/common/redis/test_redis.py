# -*- encoding: utf-8 -*-
'''
Created on 2016年11月14日

@author: huawei
'''
from redis import StrictRedis, Redis
from redis.connection import ConnectionPool
import unittest

class TestKazoo(unittest.TestCase):
#         self.kazooClient = KazooZookeeperClient("172.16.4.134:2181")

    def setUp(self):
        self.ip = "172.16.4.134"
        self.port=6379
        
    def test_strictRedis(self):
        r = StrictRedis(host=self.ip, port=self.port, db=0)
        r.set('foo', 'bar')
        r.get('foo')
              
    def test_pool(self):
        pool = ConnectionPool(host=self.ip, port=self.port, db=1,max_connections=20)
        r = Redis(connection_pool=pool)
        r.set("huawei","huawei")
        print r.get("huawei")
        r.delete("huawei")
        print r.ping()
        print r.get("huawei")
        print 2 ** 2
    
        #     def test_create_child(self):
#         if self.kazooClient.isExistPath("/huawei/huawei2/huawei1") is False:
#             self.kazooClient.create("/huawei/huawei2/huawei1", False,value="son of bitch")
#     def test_putdata(self):
#         self.kazooClient.putData("huawei", "huawei")
#     def test_getdata(self):
#         print self.kazooClient.getData("huawei")
#     def test_get_child(self):
#         print self.kazooClient.getChildren("/huawei")
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
