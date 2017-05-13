# -*- encoding: utf-8 -*-
'''
Created on 2016年7月11日

@author: hua
'''
from cabbage.job.python_script_Job import PythonScriptJob

JOB_HOLDER={
            PythonScriptJob.TYPE:PythonScriptJob
            }
class JobHolder():
    @classmethod
    def getJob(self,t):
        return JOB_HOLDER[t]
        