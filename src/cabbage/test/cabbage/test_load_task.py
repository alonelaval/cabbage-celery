# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''
from cabbage.common.cabbage.util import isCabbageTask
from importlib import import_module
import fnmatch
import imp
import inspect
import os
import sys
import unittest
class TestTask(unittest.TestCase):
    def test_impl(self):
        d="/Users/hua/workspace/python/cabbage/server_file_path/123456789"
#         sys.path.append(os.path.abspath(d))
        fs =  fnmatch.filter(os.listdir(d), '*.py')
#         print fs
#         print  sys.path
        for f in fs:
            f = f.split(".")[0]
#             import f
#             print f
#             print import_module(f)
            model_moudle = imp.find_module(f, [d])
#             print model_moudle
            moudle = imp.load_module(f, model_moudle[0], model_moudle[1], model_moudle[2])
            clsmembers = inspect.getmembers(moudle, inspect.isclass)
            
#             print "clsmembers: %s"%clsmembers
            for cls in clsmembers:
                print cls
                if isCabbageTask(cls[1]):
                    print cls[1].__module__  +"."+ cls[1].__name__
                    print cls[1].__module__ 
                
#             for name, obj in inspect.getmembers(model_moudle):
#                 print name, obj
#                 if inspect.isclass(obj):
#                     print name, obj
            
        pass
    
if __name__=="__main__":
    unittest.main()
