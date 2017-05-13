# coding: utf8
'''
Created on 2016-8-30

@author: yan.feng
'''
from cabbage.utils.host_name import getHostName
from cabbage.cabbage_celery.task import CabbageTask
from cabbage.common.log.logger import Logger
import websocket
import json
import logging
from product_detail_parser import ProductDetailParser

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

log = Logger.getLogger(__name__)
serverAddr = '10.0.137.88:8888'

productDetailParser = ProductDetailParser()

'''
    产品更新任务
'''
class ProductInfoUpdater:
    
    def __init__(self):
        websocket.enableTrace(False)
        wsPath = "ws://%s/product/ws" % serverAddr
        self.ws = websocket.create_connection(wsPath)
    
    def update(self, lid):
        self.lid = lid
        param = {'method':'getJobInfo', 'data':{'lid':lid}}
        msg = json.dumps(param)
        self.ws.send(msg)
        result = self.ws.recv()
        jsonData = json.loads(result)
        if bool(jsonData['success']):
            jobType = jsonData['data']['jobType']
            if (int(jobType) == 1001):
                productId = jsonData['data']['productId']
                if productId is not None:
                    url = 'https://item.taobao.com/item.htm?id=%s' % productId
                    data = productDetailParser.parse(url)[2]
                    if data is None:
                        data = {'productId':productId, 'valid':False}
                    data['lid'] = lid
                    self.saveToDB(data)
        self.close()
    
    '''
                    保存数据到DB
    '''
    def saveToDB(self, info):
        try:
            msg = json.dumps({'method':'addProduct', 'data':info})
            self.ws.send(msg)
            result = self.ws.recv()
            jsonData = json.loads(result)
            if bool(jsonData['success']):
                print '%s : Save product "%s" ok.' % (getHostName(), info['productId'])
        except Exception:
            log.exception(getHostName())
    
    def close(self):
        self.ws.close()
                        
        
    
class ProductInfoUpdateTask(CabbageTask):
        
    def run(self, *args, **kwargs):
        self.lid = kwargs['lid']
        if self.lid:
            updater = ProductInfoUpdater()
            updater.update(self.lid)
            
if __name__ == '__main__':
    updater = ProductInfoUpdater()
    updater.update(14)
    pass
