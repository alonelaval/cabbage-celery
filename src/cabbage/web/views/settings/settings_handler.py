# -*- encoding: utf-8 -*-
'''
Created on 2016年10月10日

@author: huawei
'''
from cabbage.web.views.base_handler import BaseHandler
class SettingsHandler(BaseHandler):
    def get(self):
        self.render("settings.html")
