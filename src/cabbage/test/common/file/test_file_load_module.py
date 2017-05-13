# -*- encoding: utf-8 -*-
'''
Created on 2016年7月11日

@author: hua
'''
from cabbage.common.cabbage.util import isCabbageTask, \
    isCabbageMain
from cabbage.common.file.load_file_holder import LoadMoudleHolder
from cabbage.config import ConfigHolder
from cabbage.constants import PYTHON, BASE, CLIENT_FILE_DIRECTORY
from cabbage.data.zookeeper_store import ZookeeperStore
import imp
import inspect
import unittest

class TestUtil(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_aaa(self):
        store=ZookeeperStore()
        jobId="123456789"
        job = store.getJob(jobId)
#         print job.filePath
        loadMoudle = LoadMoudleHolder.getLoadMoudle(PYTHON)
        clientDir = ConfigHolder.getConfig().getProperty(BASE,CLIENT_FILE_DIRECTORY)
        path = clientDir+"/"+jobId
        print path
        print job.fileName
        classes =loadMoudle.load("/Users/hua/workspace/python/cabbage/client_file_path/123456789/","test_task.py")
        
        modelMoudle = imp.find_module("test_task", [path])
        moudle = imp.load_module("test_task", modelMoudle[0], modelMoudle[1], modelMoudle[2])
        print moudle
        print dir(moudle)
        print inspect.getmembers(moudle)
        
        print classes
        for clazz in classes:
            if isCabbageMain(clazz[1]):
                print 1112
        
if __name__=="__main__":
    unittest.main()
