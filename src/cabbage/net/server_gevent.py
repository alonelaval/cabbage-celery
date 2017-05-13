# -*- encoding: utf-8 -*-
'''
Created on 2016年6月3日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, SERVER_PORT, SERVER_IP
from cabbage.net.handle_request import handleRequest
from cabbage.net.server import Server
from gevent import monkey, socket
from gevent.pool import Pool
from gevent.server import StreamServer
from zope.interface.declarations import implementer
import gevent
monkey.patch_all()
log = Logger.getLogger(__name__)

@implementer(Server)
class GeventServer():
    def __init__(self,ip="127.0.0.1",port=1024,listenMax=50):
        self.ip=ip
        self.port=port
        self.sock = socket.socket()
        self.listenMax =listenMax
    def start(self):
        server_address = (self.ip, self.port)
        self.sock.bind(server_address)
        self.sock.listen(self.listenMax)
        self.receive();
        
    def receive(self):
        while True:
            conn, addr = self.sock.accept()
            gevent.spawn(handleRequest, conn,addr)
            
    def sendall(self,conn,message):
        pass
    
    def connected(self):
        pass
    
    def stop(self):
        self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()

@implementer(Server)
class GeventStreamServer():
    def __init__(self,ip=ConfigHolder.getConfig().getProperty(BASE, SERVER_IP),port=int(ConfigHolder.getConfig().getProperty(BASE, SERVER_PORT)),maxCon=1000):
        self.pool = None  # do not accept more than 10000 connections
        self.ip=ip
        self.port=port
        
        self.maxCon =maxCon
        self.inited=False
    def start(self):
        if not self.inited:
            log.info("启动GeventStreamServer服务，端口:%s............."%self.port)
            self.pool = Pool(self.maxCon)
            self.inited =True
            self.server=StreamServer((self.ip, self.port), handleRequest, spawn=self.pool)
            self.server.serve_forever()
            
        
    def connected(self):
        return not self.server.closed()
        
    def stop(self):
        self.server.close()
