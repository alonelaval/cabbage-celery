'''
Created on 2016-10-17

@author: admin
'''
from cabbage.cabbage_celery.main import CabbageMain
from cabbage.common.log.logger import Logger
import os

log = Logger.getLogger(__name__)

class ProductListCrawlerMain(CabbageMain):
    def run(self, *args, **kwargs):
#         shopUrl = args[0]
#         log.info("shopUrl: %s" % shopUrl)
        
        p = os.path.join(os.path.dirname(__file__),"taobaoshop.txt") 
        with open(p,"r+") as reader:
            for line in reader :
                shopUrl = "http://%s.taobao.com"%line.strip()
                self.send_task("bc_shop_crawler.BcShopCrawlerTask", kwargs={'shopUrl': shopUrl})
                break



if __name__=="__main__":
    ProductListCrawlerMain().run()