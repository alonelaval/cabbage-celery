# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, LOG_CONFIG_PATH
from cabbage.utils.host_name import HOST_NAME
import logging.config
import os

class Logger():
    logging.config.fileConfig( ConfigHolder.getConfig().getProperty(BASE,LOG_CONFIG_PATH))
    loggers={}
    @classmethod
    def getLogger(self,key):
        if key in Logger.loggers:
            return Logger.loggers[key]
        else:
            logger = logging.getLogger(key)
            Logger.loggers[key] =logger
            return logger
     
    @classmethod   
    def info(self,log,message): 
        log.info("【%s】: %s"%(HOST_NAME,message))
    
    @classmethod   
    def debug(self,log,message): 
        log.debug("【%s】: %s"%(HOST_NAME,message))
    
    @classmethod   
    def error(self,log,message): 
        log.error("【%s】: %s"%(HOST_NAME,message))
    
    @classmethod   
    def exception(self,log): 
        log.exception("【%s】:" %HOST_NAME)
    
#     @classmethod
#     def info(self,msg):
#         logging.info(msg)
#         
#     @classmethod
#     def debug(self,msg):
#         logging.debug(msg)
#     @classmethod
#     def error(self,msg):
#         logging.error(msg)
