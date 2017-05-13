# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from cabbage.common.cache.cache_holder import CacheHolder
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, CLIENT_FILE_DIRECTORY, JOBS, \
    SERVER_FILE_DIRECTORY, DONE
from cabbage.data.store_factory import storeFactory
from cabbage.data.store_holder import StoreHolder
from cabbage.message.action.action import AbstractAction
from cabbage.message.file_message import FileResponseMessage
import os
log = Logger.getLogger(__name__)
import base64
class RequestFileAction(AbstractAction):
    def run(self):
        
        jobId=self.message.jobId
        fileName = self.message.fileName
        serverDir = ConfigHolder.getConfig().getProperty(BASE,SERVER_FILE_DIRECTORY)
        jobDir = serverDir+"/"+jobId
        filePath = jobDir+"/"+fileName
#         job =None
        with storeFactory.store() as sotre:
            job =   sotre.getJob(jobId)#StoreHolder.getServerStore().getJob(jobId)#CacheHolder.getCache().get(jobId,JOBS)
        msg = FileResponseMessage()
        msg.fileName=fileName
        msg.jobId=jobId
        if self.message.type ==self.message.MAIN:
            if fileName == job.fileName:
                f = open(filePath)
                msg.fileContent=base64.encodestring(f.read())
                f.close()
            return msg
        if self.message.type ==self.message.ATTACH:
            for attachFile in job.attachFiles:
                if attachFile.fileName == fileName:
                    f = open(filePath)
                    msg.fileContent=base64.encodestring(f.read())
                    f.close()
                    break
            return msg
        
class ResponseFileAction(AbstractAction):
    def run(self):
        clientDir = ConfigHolder.getConfig().getProperty(BASE,CLIENT_FILE_DIRECTORY)
        jobId=self.message.jobId
        jobDir = clientDir+"/"+jobId
        fileName = self.message.fileName
        fileContent = self.message.fileContent
        if os.path.exists(jobDir) is False:
            os.mkdir(jobDir)
            os.mkdir(jobDir+"/result")
        filePath = jobDir+"/"+fileName
        if os.path.exists(filePath):
            os.remove(filePath)
        f =open(filePath,"w")
        f.write(base64.decodestring(fileContent))
        f.close()
        #need notify file is ready and all file is ready 
        #then  notify server this client to be ready exec job
        CacheHolder.getCache().put(fileName, DONE, jobId)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
       
        
        
    