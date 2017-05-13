# -*- encoding: utf-8 -*-
'''
Created on 2016年7月29日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, SERVER_WEB_PORT
from cabbage.web.settings import settings
from cabbage.web.views.config.conifg_handler import ConfigHandler
from cabbage.web.views.job.job_run_list_handler import \
    JobRunListHandler
from cabbage.web.views.job.new_job_handler import NewJobHandler
from cabbage.web.views.job_handler import JobRunHandler, \
    JobListHandler, JobListDataHandler, RemoveJobListHandlder
from cabbage.web.views.main_handler import MainHandler
from cabbage.web.views.queues.add_broker_queue_handler import \
    AddBrokerQueueHandler
from cabbage.web.views.queues.add_broker_queue_node_handler import \
    AddBrokerQueueNodeHandler
from cabbage.web.views.queues.add_broker_server_handler import \
    AddBrokerServerHandler
from cabbage.web.views.queues.broker_queue_handler import \
    BrokerQueueHandler, BrokerQueueByHostNameListHandler
from cabbage.web.views.queues.broker_server_handler import \
    BrokerServerHandler
from cabbage.web.views.settings.settings_handler import \
    SettingsHandler
from cabbage.web.views.work.work_status_handler import \
    WorkStatusHandler
from cabbage.web.views.work_handler import WorkListHandler
from tornado.httpserver import HTTPServer
import os
import tornado
log = Logger.getLogger(__name__)
class CabbageApplication(tornado.web.Application):
    def __init__(self, handlers=None, default_host="", transforms=None,
                 **settings):
        super(type(self),self).__init__(handlers=handlers,default_host=default_host,transforms=transforms,**settings)
        
    def test(self):
        pass
    

class CabbageApplicationContorl(object):
    
    def start(self):
        log.info("启动web服务.........")
        application = CabbageApplication([
            (r"/", MainHandler),
            (r"/toNewJob", NewJobHandler),
            (r"/runJob", JobRunHandler),
            (r"/jobList", JobListHandler),
            (r"/jobRunList", JobRunListHandler),
            (r"/jobListData", JobListDataHandler),
            (r"/removeJob", RemoveJobListHandlder),
            (r"/work/list", WorkListHandler),
            (r"/work/workStatusChange", WorkStatusHandler),
            (r"/queues/brokerServer", BrokerServerHandler),
            (r"/queues/brokerQueue", BrokerQueueHandler),
            (r"/queues/selectQueue", BrokerQueueByHostNameListHandler),
            (r"/queues/addQueue", AddBrokerQueueHandler),
            (r"/queues/addQueueNode", AddBrokerQueueNodeHandler),
            (r"/queues/addBrokerServer", AddBrokerServerHandler),
            (r"/config", ConfigHandler),
            (r"/settings", SettingsHandler),
            
            
        ], debug=False,**settings)
      
        
        port =ConfigHolder.getConfig().getProperty(BASE, SERVER_WEB_PORT)
#         application.listen(int(port))
        
        sockets = tornado.netutil.bind_sockets(port)
        tornado.process.fork_processes(8)
        server = HTTPServer(application)
        server.add_sockets(sockets)
        log.info("web服务启动成功,端口：%s........."%port)

if __name__ == "__main__":
#     application = CabbageApplication([
#         (r"/", MainHandler),
#         (r"/toNewJob", NewJobHandler),
#     ], debug=True,**settings)
#     application.listen(8888)
    CabbageApplicationContorl().start()
    print os.getpid()
#     print id(ZookeeperClientHolder.getRetryClient())
    tornado.ioloop.IOLoop.current().start()