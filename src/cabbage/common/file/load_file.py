# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''
from zope.interface.interface import Interface
from cabbage.utils.util import singleton
import imp
import inspect
import os
from zope.interface.declarations import implementer

class LoadMoudle(Interface):
    '''
        加载模块
    '''
    def load(self,directory,fileName):
        pass

@singleton
@implementer(LoadMoudle)    
class LoadPythonMoudle():
    def load(self,directory,fileName):
        if directory and fileName:
            if os.path.isdir(directory) and os.path.isfile(directory+"/"+fileName):
                import sys
                sys.path.append(directory) 
                fileName=fileName.replace(".py","")
                modelMoudle = imp.find_module(fileName, [directory])
                moudle = imp.load_module(fileName, modelMoudle[0], modelMoudle[1], modelMoudle[2])
                return inspect.getmembers(moudle, inspect.isclass)
            else:
                raise Exception("file not found!")

