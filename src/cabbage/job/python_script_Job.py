# -*- encoding: utf-8 -*-
'''
Created on 2016年7月11日

@author: huawei
'''
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.cabbage_celery.util import isCabbageMain
from cabbage.common.file.load_file_holder import LoadMoudleHolder
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import PYTHON, BASE, SERVER_FILE_DIRECTORY
from cabbage.job.Job import AbstractJob
log = Logger.getLogger(__name__)
class PythonScriptJob(AbstractJob):
    TYPE=PYTHON
    def __init__(self,job):
        super(PythonScriptJob,self).__init__(job)
        self.mainClass=self._loadMain()
        if self.mainClass is None:
            raise Exception("job:%s not mainClass!"%self.job.jobName)
        self.mainObj = self.mainClass()
        self.isRun =False
        self.results= self.mainObj.results
        self.mainObj.job=self.job
        
    def name(self):
        return self.job.jobName
    
    def stop(self):
        for taskName in self.job.tasks:
            CabbageHolder.getServerCabbage(self.job.brokerServer).revokeByTaskName(taskName)
        self.isRun =False
        
    def restart(self):
        if not self.isRun:
            self.start()
            
    def pause(self):
        pass
    def forward(self):
        pass
    
    def start(self,params=None):
        if self.mainObj is None:
            raise Exception("job:%s not mainClass!"%self.job.jobName)
        self.isRun = True
        self.mainObj.run(params)
        
    def _loadMain(self):
        serverDir = ConfigHolder.getConfig().getProperty(BASE,SERVER_FILE_DIRECTORY)
        path = serverDir+"/"+self.job.jobId
        loadMoudle = LoadMoudleHolder.getLoadMoudle(PYTHON)
        classes =loadMoudle.load(path,self.job.fileName)
        for clazz in classes:
            obj = clazz[1]
            if isCabbageMain(obj):
                return obj
        return None
        