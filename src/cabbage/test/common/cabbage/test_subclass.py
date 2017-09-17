# -*- encoding: utf-8 -*-
'''
Created on 2016年6月13日

@author: hua
'''

# from cabbage.cabbage_celery.main import CabbageMain
from cabbage.common.cabbage_celery.util import isCabbageMain
from cabbage.common.cabbage_celery.util import isCabbageTask
from cabbage.common.file.load_file_holder import LoadMoudleHolder
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, SERVER_FILE_DIRECTORY, PYTHON
import unittest

def loadMain():
        serverDir = ConfigHolder.getConfig().getProperty(BASE,SERVER_FILE_DIRECTORY)
        path = "/Users/hua/workspace/mypython/cabbage/samples"
        loadMoudle = LoadMoudleHolder.getLoadMoudle(PYTHON)
        classes =loadMoudle.load(path,"test_both_task.py")
        for clazz in classes:
            obj = clazz[1]
            print obj
            if isCabbageTask(obj):
                print obj
                return obj
        return None

def loadTasks():
           
        
class TestSubClass(unittest.TestCase):
    def test_put(self):
#         print isCabbageMain(CabbageMain)
        print loadMain()
    
if __name__=="__main__":
    unittest.main()
