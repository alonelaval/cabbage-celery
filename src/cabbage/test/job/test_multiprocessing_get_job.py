# -*- encoding: utf-8 -*-
'''
Created on 2016年7月27日

@author: hua
'''
from cabbage.data.store_holder import StoreHolder
import multiprocessing
import os
import unittest

def worker():
    print "worker_pid:%d"% os.getpid()
    job = StoreHolder.getStore().getJob("123456789")
    print StoreHolder.getStore()
    print job.fileName
    
class TestAddTask(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_aaa(self):
        for i in range(10):
            p2 = multiprocessing.Process(target = worker)
            p2.start()
            p2.join()

if __name__=="__main__":
    unittest.main()
    