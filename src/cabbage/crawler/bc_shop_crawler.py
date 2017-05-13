'''
Created on 2016-10-17

@author: admin
'''
from cabbage.cabbage_celery.task import CabbageTask
from cabbage.common.log.logger import Logger
import json
import traceback
import websocket
import requests

from shop_detail import getShopDetail

log = Logger.getLogger(__name__)
serverAddr = '172.16.4.1:8888'

class BcShopCrawler(object):
    
    def __init__(self):
        websocket.enableTrace(False)
        wsPath = "ws://%s/bcshop/ws" % serverAddr
        self.ws = websocket.create_connection(wsPath)
    
    def runEachUrl(self, url):
        if url:
            try:
                data = getShopDetail(url.strip())
                if data is not None:
                    param = {'method':'saveBcShop', 'data': data}
                    msg = json.dumps(param)
                    self.ws.send(msg)
                    result = self.ws.recv()
                    jsonData = json.loads(result)
                    if bool(jsonData['success']):
                        log.info('%s save ok.' % url)
            except:
                traceback.print_exc()
    
    def run(self, filePath):
        try:
            with open(filePath) as urlList:
                for shopUrl in urlList:
                    log.info('Get shop by url: %s' % shopUrl)
                    self.runEachUrl(shopUrl)
        except:
            traceback.print_exc()
        self.close()
        print 'completed'
    
    def close(self):
        self.ws.close()
    
    def test(self, filePath):
        print 'Test only.'
        #url = "http://192.168.109.38:2048/runJob"
        url = 'http://101.198.156.26:2048/runJob'
        jobId = "job-8fcde4b5-65ff-4860-9138-dd63b433132d"
        shopUrl= 'https://shop100002159.taobao.com'
        try:
            requests.post(url, data={'jobId':jobId, "params":shopUrl})
        except:
            traceback.print_exc()
        print 'completed'
        
        
class BcShopCrawlerTask(CabbageTask): 
        
    def doRun(self, *args, **kwargs):
        shopUrl = kwargs['shopUrl']
        if shopUrl:
            crawler = BcShopCrawler()
            crawler.runEachUrl(shopUrl)
            

if __name__ == '__main__':
    filePath = 'd:/taobaoshop.txt'
    crawler = BcShopCrawler()
    shopUrl = 'https://shop34016263.taobao.com'
    crawler.runEachUrl(shopUrl)
    #crawler.test(filePath);
    pass
