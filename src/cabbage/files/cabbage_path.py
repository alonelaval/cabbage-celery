# -*- encoding: utf-8 -*-
'''
Created on 2016年9月21日

@author: huawei
'''
from cabbage.config import ConfigHolder
from cabbage.constants import CABBAGE, NODE, MASTER, BASE, \
    SERVER_FILE_DIRECTORY, CLIENT_FILE_DIRECTORY
import os



def getLocalFilesPath():
    serverType = os.environ.get(CABBAGE) 
    if serverType == NODE:
        return ConfigHolder.getConfig().getProperty(BASE,CLIENT_FILE_DIRECTORY)
    elif serverType == MASTER:
        return ConfigHolder.getConfig().getProperty(BASE,SERVER_FILE_DIRECTORY)