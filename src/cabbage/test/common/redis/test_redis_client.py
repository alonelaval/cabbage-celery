# -*- encoding: utf-8 -*-
'''
Created on 2016年11月18日

@author: huawei
'''
# -*- encoding: utf-8 -*-
from cabbage.common.redis.redis_client import RedisClient
import unittest
'''
Created on 2016年6月3日

@author: hua
'''


class TestRedisClient(unittest.TestCase):
#         self.kazooClient = KazooZookeeperClient("172.16.4.134:2181")

    def setUp(self):
        self.redisClient = RedisClient("10.0.137.87")
#
    def test_delete(self):
#         self.redisClient.delete("huawei")
# #     
        pass
    def test_isConnected(self):
        pass
#         print self.redisClient.isConnected()
        
    def test_get(self):
        pass
#         print self.redisClient.get("huawei")
# #     
    def test_put(self):
        for i in range(30):
            self.redisClient.put("huawei%s"%i, i)
#         for i in range(30000):
#             self.redisClient.delete("huawei%s"%i)
#         self.redisClient.put("huawei", "fuck you!",ex=60)
        
if __name__=="__main__":
    unittest.main()
