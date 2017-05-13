# -*- encoding: utf-8 -*-
'''
Created on 2016年10月10日

@author: huawei
'''
# from cabbage.common.cache.cache_holder import CacheHolder
# from cabbage.constants import WORKS, REMOVE, ON_LINE, OFF_LINE
# from cabbage.machine.celery_work_contorl import CeleryWorkContorl
from cabbage.web.api.work_api import WorkApi
from cabbage.web.views.base_handler import BaseHandler

class WorkStatusHandler(BaseHandler):
    def post(self):
        hostName = self.getArgument("hostName")
        status = self.getArgument("status")
        if hostName:
            work =WorkApi().getWork(hostName) # CacheHolder.getCache().get(hostName,WORKS)
            if work:
                WorkApi().workChangeStatus(work, status)
#                 if status == REMOVE:
#                     CeleryWorkContorl(work).stop()
#                 if status == ON_LINE:
#                     CeleryWorkContorl(work).startService()
#                 if status == OFF_LINE:
#                     CeleryWorkContorl(work).stopService()
                    
    