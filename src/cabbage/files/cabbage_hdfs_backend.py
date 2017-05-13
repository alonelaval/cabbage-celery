# -*- encoding: utf-8 -*-
'''
Created on 2016年10月11日

@author: huawei
'''
from cabbage.common.hdfs.hdfs_client_holder import \
    HdfsClientHolder
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, HDFS_ROOT_PATH, CABBAGE, \
    MASTER, NODE
from cabbage.files.cabbage_backend import \
    AbstractCabbageFileSystemBackend
from cabbage.files.cabbage_path import getLocalFilesPath
from cabbage.utils.date_util import getNowDateStr, getNowHour, \
    subDay, getNow, formatDate
from cabbage.utils.host_name import HOST_NAME,LOCAL_IP
import os

log=Logger.getLogger(__name__)

class CabbageHdfsBackend(AbstractCabbageFileSystemBackend):
    def __init__(self,jobId):
        super(CabbageHdfsBackend,self).__init__(jobId)
        
    def save(self):

        hdfsPath=ConfigHolder.getConfig().getProperty(BASE,HDFS_ROOT_PATH)
       
        dateStr = getNowDateStr()
        if self.jobId:
            localPath = getLocalFilesPath()
            dateStr = getNowDateStr()
            hour = getNowHour()
            
            if hour == 0:# 提交前一天的数据
                dateStr = formatDate(subDay(getNow(),1),f="%Y%m%d")
            
            p = localPath+"/"+self.jobId+"/result/"+dateStr
            Logger.debug( log, "upload file to hdfs. jobId【%s】 date【%s】" % (self.jobId,dateStr))
            if not  os.path.isdir(p):
                return
            
            fileNames = os.listdir(p)
            if len(fileNames) == 0:
                return
            
            client =HdfsClientHolder.getHdfsClient()
            remoteDire=hdfsPath+"/"+self.jobId
            
            if not client.isDirectory(remoteDire):
                client.mkdir(remoteDire)
            remoteDire= remoteDire+"/"+dateStr
            
            if not client.isDirectory(remoteDire):
                client.mkdir(remoteDire)
            Logger.info(log,"hour:%s  files:%s"%(hour,",".join(fileNames)))
            for fileName in fileNames:
                
                if hour != 0:
                    if int(fileName) >= hour:
                        continue
#                 if os.path.isfile(p+"/"+fileName):
            
                self.uploadToHdfs(client,localPath,self.jobId,hdfsPath,fileName,dateStr)
                os.remove(p+"/"+fileName)
                    
    def uploadToHdfs(self,client,localPath,jobId,hdfsPath,fileName,dateStr):
        
            
        localFile = localPath+"/"+jobId+"/result/"+dateStr+"/"+fileName
        if os.environ[CABBAGE] ==MASTER:
            fileName = HOST_NAME+"_"+LOCAL_IP+"_"+MASTER+"_"+fileName
        else:
            fileName = HOST_NAME+"_"+LOCAL_IP+"_"+NODE+"_"+fileName
            
        remoteDire=hdfsPath+"/"+self.jobId+"/"+dateStr
        
        client.upload(localFile,remoteDire+"/"+fileName)
