# -*- encoding: utf-8 -*-
'''
Created on 2016年7月4日

@author: hua
'''
# from zope.interface.interface import Interface
from cabbage.common.file.load_file import LoadPythonMoudle
from cabbage.constants import PYTHON
LOADS={PYTHON:LoadPythonMoudle()}
class LoadMoudleHolder:
    @classmethod
    def getLoadMoudle(cls,t=PYTHON):
        return LOADS[t]