# -*- encoding: utf-8 -*-
'''
Created on 2016年8月24日

@author: huawei
'''
from cabbage.web.api.work_api import WorkApi
from cabbage.web.views.base_handler import BaseHandler
import json
class WorkListHandler(BaseHandler):
    def get(self):
        self.render("work_list.html")
    def post(self):
        works =WorkApi().getWorks()
#         m ={}
#         m["total"]= len(works)
#         m["rows"]=[w.asDict() for w in works]
        self.write( json.dumps([w.asDict() for w in works]))