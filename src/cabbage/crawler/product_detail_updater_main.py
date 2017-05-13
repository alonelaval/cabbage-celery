'''
Created on 2016-8-30

@author: admin
'''
from __future__ import absolute_import
from cabbage.cabbage_celery.main import CabbageMain
from cabbage.common.log.logger import Logger
log = Logger.getLogger(__name__)

class ProductListCrawlerMain(CabbageMain):
    
    def run(self, *args, **kwargs):
        lid=args[0]
        log.info("lid:%s"%lid)
        
        self.send_task("product_detail_updater.ProductInfoUpdateTask", kwargs={'lid': lid})
#         task =self.getApp().send_task("product_detail_updater.ProductInfoUpdateTask",kwargs={'lid': lid})
#         self.addResult(task)