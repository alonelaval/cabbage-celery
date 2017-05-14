# -*- encoding: utf-8 -*-
'''
Created on 2016年8月31日

@author: huawei
'''
from cabbage.web.api.broker_queue_api import BrokerQueueApi
from cabbage.web.api.broker_server_api import BrokerServerApi
from cabbage.web.api.work_api import WorkApi
from cabbage.web.views.base_handler import BaseHandler
from cabbage.web.views.json_result import JsonResult
import json
import tornado
class BrokerQueueHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("queues/broker_queue.html",works=WorkApi().getWorks(),servers=BrokerServerApi().getBrokerServers())
    @tornado.web.authenticated    
    def post(self):
        queues = BrokerQueueApi().getBrokerQueue()
        
        if queues:
            serverList=[s.asDict() for s in queues] 
            self.write( json.dumps(serverList))
            
        
class BrokerQueueByHostNameListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        hostName = self.getArgument("hostName")
        jsonResult =JsonResult()
        try: 
            if hostName:
                jsonResult.result=JsonResult.RESULT_SUCCESS
                jsonResult.data =BrokerServerApi().getBrokerServerByHostname(hostName).queues
                jsonResult.message ="查找服务器成功！"
                self.write(jsonResult.asDict())
                return 
            else:
                jsonResult.result=JsonResult.RESULT_PARAM_ERROR
                jsonResult.message ="参数错误！"
                self.write(jsonResult.asDict())
        except Exception  as e:
            jsonResult.result=JsonResult.RESULT_UNKNOWN_ERROR
            jsonResult.message ="查找服务器失败，原因：%s！" % str(e)
            self.write(jsonResult.asDict())
    @tornado.web.authenticated        
    def post(self):
        self.get()
