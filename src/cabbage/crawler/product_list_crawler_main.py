'''
Created on 2016-8-10

@author: admin
'''
from __future__ import absolute_import
# from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.cabbage_celery.main import CabbageMain
from cabbage.common.log.logger import Logger
# from zope.interface.declarations import implementer
log = Logger.getLogger(__name__)

class ProductListCrawlerMain(CabbageMain):
    def run(self, *args, **kwargs):
#         print args
        lid=args[0]
        log.info("lid:%s"%lid)
        
        self.send_task("product_list_crawler.ProductListCrawlerTask", kwargs={'lid': lid})
      
#         task = self.getApp().send_task("product_list_crawler.ProductListCrawlerTask",kwargs={'lid': lid})
#         self.addResult(task)
#         task = ProductListCrawlerTask()
#         result = task.delay(lid=lid)
#         print "main:" + str(result)
#         while(1):
#             if result.ready():
#                 print "result:" + str(result.result)
#                 break
#             if result.failed():
#                 print "result:" + str(result.result)
#                 break
#             print result.status
#             time.sleep(2)
