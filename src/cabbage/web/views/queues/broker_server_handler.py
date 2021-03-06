# -*- encoding: utf-8 -*-
'''
Created on 2016年8月31日

@author: huawei
'''
from cabbage.web.api.broker_server_api import BrokerServerApi
from cabbage.web.views.base_handler import BaseHandler
import json
import tornado
class BrokerServerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("queues/broker_server.html")
    @tornado.web.authenticated    
    def post(self):
        servers = BrokerServerApi().getBrokerServers()
        if servers:
            serverList=[s.asDict() for s in servers] 
            self.write( json.dumps(serverList))
