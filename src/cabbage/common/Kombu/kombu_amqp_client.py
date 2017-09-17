# -*- encoding: utf-8 -*-
'''
Created on 2016年8月29日

@author: huawei
'''
from kombu import Connection, Exchange, Queue


class KombuClient(object):
    def __init__(self,url="amqp://172.16.4.134"):
        self.url= url
        self.conn = Connection(self.url)
       
    
    def addQueue(self,queueName,exchangeName=None,routingKey=None,priority=1):
        self._connect()
        exchangeName = exchangeName if exchangeName else queueName
        routingKey = routingKey if routingKey else queueName
        
        science_news = Queue(queueName,exchange=Exchange(exchangeName),routing_key=routingKey,max_priority=priority)
        chan = self.conn.channel()
        try:
            bound_science_news = science_news(chan)
            bound_science_news.declare()
        finally: 
            chan.close()
            self._release()
        
    def deleteQueue(self,queueName,exchangeName):
        self._connect()
        science_news = Queue(queueName)
        chan = self.conn.channel()
        try:
            bound_science_news = science_news(chan)
            bound_science_news.delete()
        finally: 
            chan.close()
            self._release()
            
    def deleteExchage(self,exchangeName):
        self._connect()
        chan = self.conn.channel()
        bound_exchange = Exchange(exchangeName)
        try:
            bound_exchange=bound_exchange(chan)
            bound_exchange.delete()
        finally: 
            chan.close()
            self._release()
            
    def sendMessage(self,exchangeName,message,routingKey=None):
        self._connect()
        chan = self.conn.channel()
        bound_exchange = Exchange(exchangeName)
        routingKey = routingKey if routingKey else exchangeName
        try:
            bound_exchange=bound_exchange(chan)
            message = bound_exchange.Message(message)
            bound_exchange.publish(message,routingKey)
        finally: 
            chan.close()
            self._release()
        
        
    def clearQueue(self,queueName):
        self._connect()
        science_news = Queue(queueName)
        chan = self.conn.channel()
        try:
            bound_science_news = science_news(chan)
            bound_science_news.purge()
        finally: 
            chan.close()
            self._release()
        
    def _connect(self):
        self.conn.connect()
    
    def _release(self):
        self.conn.release()