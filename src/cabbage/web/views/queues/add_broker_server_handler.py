# -*- encoding: utf-8 -*-
'''
Created on 2016年9月1日

@author: huawei
'''
from cabbage.common.log.logger import Logger
from cabbage.web.api.broker_server_api import BrokerServerApi
from cabbage.web.views.base_handler import BaseHandler
log = Logger.getLogger(__name__)
        
class AddBrokerServerHandler(BaseHandler):
    def post(self):
        hostName = self.getArgument("hostName")
        ip  = self.getArgument("ip")
        port = self.getArgument("port")
        connectUri = self.getArgument("connectUri")
        serverType  = self.getArgument("serverType")
        
        try: 
            if hostName and connectUri and ip and port and serverType:
                brokerApi= BrokerServerApi()
                
                brokerApi.addServer(hostName, ip, port, connectUri, serverType)
                
                self.render("queues/broker_server.html",message="添加成功！")
            else:
                self.render("queues/broker_server.html",errorMessage="参数错误！")
        except Exception  as e:
            log.exception(e)
            self.render("queues/broker_server.html",errorMessage="添加队列服务器失败，原因：%s！" % str(e))
            