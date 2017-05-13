#-*- coding: UTF-8 -*- 
'''
Created on 2016年7月21日

@author: huawei
'''
# from cabbage.common.scheduler.scheduler import jobMange
from cabbage.common.scheduler.scheduler import JobManage

class JobManageHolder():
    @classmethod
    def getJobManage(self):
        return JobManage()