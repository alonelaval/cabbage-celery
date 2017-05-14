# -*- encoding: utf-8 -*-
'''
Created on 2016年10月10日

@author: huawei
'''
from cabbage.web.views.base_handler import BaseHandler
import tornado
class SettingsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("settings.html")
