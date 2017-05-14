# -*- encoding: utf-8 -*-
'''
Created on 2016年9月1日

@author: huawei
'''
from cabbage.common.log.logger import Logger
from cabbage.web.api.broker_queue_api import BrokerQueueApi
from cabbage.web.api.broker_server_api import BrokerServerApi
from cabbage.web.api.work_api import WorkApi
from cabbage.web.views.base_handler import BaseHandler
import tornado
import traceback
# from cabbage.web.views.json_result import JsonResult
log = Logger.getLogger(__name__)
        
class AddBrokerQueueHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        brokerServer = self.getArgument("brokerServer")
        brokerQueue  = self.getArgument("brokerQueue")
        exchange = self.getArgument("exchange")
        routingKey = self.getArgument("routingKey")
        nodes  = self.get_arguments("nodes")
        
        try: 
            if brokerServer and brokerQueue:
                brokerApi= BrokerQueueApi()
                if brokerApi.isExistQueueName(brokerQueue):
                    raise Exception("队列名称已经存在！")
                
                brokerApi.addQueue(brokerServer, brokerQueue, exchange, routingKey, nodes)
                
#                 print brokerQueue,routingKey,exchange,nodes
                self.render("queues/broker_queue.html",message="添加成功！",works=WorkApi().getWorks(),servers=BrokerServerApi().getBrokerServers())
            else:
                self.render("queues/broker_queue.html",errorMessage="参数错误！",works=WorkApi().getWorks(),servers=BrokerServerApi().getBrokerServers())
        except Exception  as e:
            traceback.print_exc()
            log.exception(e)
            
            self.render("queues/broker_queue.html",errorMessage="添加队列失败，原因：%s！" % str(e),works=WorkApi().getWorks(),servers=BrokerServerApi().getBrokerServers())