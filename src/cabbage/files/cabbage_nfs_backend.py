# -*- encoding: utf-8 -*-
'''
Created on 2016年10月11日

@author: huawei
'''


from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, NFS_DIRECTORY, CABBAGE, MASTER, \
    NODE
from cabbage.files.cabbage_backend import \
    AbstractCabbageFileSystemBackend
from cabbage.files.cabbage_path import getLocalFilesPath
from cabbage.utils.date_util import getNowDateStr, getNowHour, \
    subDay, getNow, formatDate
from cabbage.utils.host_name import HOST_NAME, LOCAL_IP
import os
import shutil

log=Logger.getLogger(__name__)

class CabbageNfsBackend(AbstractCabbageFileSystemBackend):
    def __init__(self,jobId):
        super(CabbageNfsBackend,self).__init__(jobId)
        
    def save(self):
        try:
            nfsPath=ConfigHolder.getConfig().getProperty(BASE,NFS_DIRECTORY)
            dateStr = getNowDateStr()
            if self.jobId:
                localPath = getLocalFilesPath()
                dateStr = getNowDateStr()
                hour = getNowHour()
                
                if hour == 0:# 提交前一天的数据
                    dateStr = formatDate(subDay(getNow(),1),f="%Y%m%d")
                
                localPath = localPath+"/"+self.jobId+"/result/"+dateStr
                
                Logger.info( log, "upload file to nfs. jobId【%s】 date【%s】" % (self.jobId,dateStr))
                if not  os.path.isdir(localPath):
                    return
                
                fileNames = os.listdir(localPath)
                if len(fileNames) == 0:
                    return
                
                remoteDire=nfsPath+"/"+self.jobId+"/"+dateStr
                
                if not os.path.isdir(remoteDire):
                    os.makedirs(remoteDire)
    #                 os.chmod(remoteDire,777)
                Logger.info(log,"hour:%s  files:%s"%(hour,",".join(fileNames)))
                for fileName in fileNames:
                    if hour != 0:
                        if int(fileName) >= hour:
                            continue
                        
                    newFileName = None
                    if os.environ[CABBAGE] ==MASTER:
                        newFileName = HOST_NAME+"_"+LOCAL_IP+"_"+MASTER+"_"+fileName
                    else:
                        newFileName = HOST_NAME+"_"+LOCAL_IP+"_"+NODE+"_"+fileName
                    
                    if os.path.isfile(localPath+"/"+fileName):
                        shutil.move(localPath+"/"+fileName,remoteDire+"/"+newFileName)
                        
        except Exception as e:
            Logger.exception(log)
                    
                    