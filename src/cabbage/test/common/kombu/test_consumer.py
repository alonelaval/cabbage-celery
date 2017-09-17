# -*- encoding: utf-8 -*-
'''
Created on 2016年8月29日

@author: huawei
'''

from cabbage.common.Kombu.kombu_amqp_client import KombuClient
from kombu.entity import Queue, Exchange
import unittest
def process_media(body, message):
        print body
        message.ack()
        
class TestKombu(unittest.TestCase):
#     def testAddQueue(self):
#         client = KombuClient()
#         client.addQueue("huawei", "huawei", "huawei")
        
#     def test_sendMessage(self):
#         client = KombuClient()
#         client.sendMessage("huawei","huawei", "huawei")
        
#     def test_clearQueue(self):
#         client = KombuClient()
#         client.clearQueue("huawei")
  
    #amqp://cabbage_celery_url:cabbage_celery_url@123.59.211.146:5672/cabbage_vhost_url
    #amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost
    def testUrl(self):
        client = KombuClient(url="amqp://cabbage_celery:cabbage_celery@172.16.4.134:5672/cabbage_vhost")
        conn = client.conn
        conn.connect()
        video_queue = Queue('celery', exchange=Exchange("celery"), routing_key='celery')
        with conn.Consumer(video_queue, callbacks=[process_media],accept=['json', 'pickle', 'msgpack', 'yaml']) as consumer:
        # Process messages and handle events on all channels
            while True:
                conn.drain_events()
        

    
         
if __name__=="__main__":
    unittest.main()