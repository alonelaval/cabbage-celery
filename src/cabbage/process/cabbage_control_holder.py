# -*- encoding: utf-8 -*-
'''
Created on 2016年7月26日

@author: hua
'''
from cabbage.process.cabbage_celery_control import CabbageControl
class CabbageControlHolder():
    @classmethod
    def getCabbageControl(cls):
        return CabbageControl()
        