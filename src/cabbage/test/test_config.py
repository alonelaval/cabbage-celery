# -*- encoding: utf-8 -*-
'''
Created on 2016年6月8日

@author: hua
'''
import ConfigParser
import os
import unittest

class TestKazoo(unittest.TestCase):
#         self.kazooClient = KazooZookeeperClient("172.16.4.134:2181")

    def test_reader(self):
        cfg = ConfigParser.ConfigParser()
        cfg.read(os.getcwd().split("cabbage")[0]+'cabbage/cabbage.cfg')
        print cfg.get("base", "zookeeper")
        print cfg.get("base", "serverFileDirectory")
        print cfg.has_option("base", "daa")
        
if __name__=="__main__":
        unittest.main()
