# -*- encoding: utf-8 -*-
'''
Created on 2016年6月13日

@author: hua
'''

from cabbage.cabbage_celery.main import CabbageMain
from cabbage.common.cabbage.util import isCabbageMain
from cabbage.common.file.load_file_holder import LoadMoudleHolder
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, SERVER_FILE_DIRECTORY, PYTHON
from cabbage.crawler.product_list_crawler_main import \
    ProductListCrawlerMain
import unittest

def loadMain():
        serverDir = ConfigHolder.getConfig().getProperty(BASE,SERVER_FILE_DIRECTORY)
        path = serverDir+"/job-06a4c37e-3ca2-46cb-9344-9f23fc03e8c7"
        loadMoudle = LoadMoudleHolder.getLoadMoudle(PYTHON)
        classes =loadMoudle.load(path,"product_list_crawler_main.py")
        for clazz in classes:
            obj = clazz[1]
            print clazz
            if isCabbageMain(obj):
                return obj
        return None
        
        
class TestSubClass(unittest.TestCase):
    def test_put(self):
        print isCabbageMain(CabbageMain)
        print loadMain()()
    
if __name__=="__main__":
    unittest.main()
