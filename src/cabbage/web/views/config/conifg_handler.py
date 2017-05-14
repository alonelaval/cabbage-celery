# -*- encoding: utf-8 -*-
'''
Created on 2016年9月27日

@author: huawei
'''
from cabbage.web.api.config_api import ConfigApi
from cabbage.web.views.base_handler import BaseHandler
import json
import tornado

class ConfigHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("config/config.html")
    @tornado.web.authenticated    
    def post(self):
        configs =ConfigApi().getConfigs()
        
        if configs:
            self.write( json.dumps([s.asDict() for s in configs]))
