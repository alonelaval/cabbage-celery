# -*- encoding: utf-8 -*-
'''
Created on 2016年6月7日

@author: hua
'''
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, SERVER_IP, SERVER_PORT
from cabbage.message.message_codec import MessageCodec, Codec
from cabbage.message.message_holder import MESSAGE_HOLDER
from cabbage.net.handle_request import RECV_LEN, doRequestHandle
from zope.interface.declarations import implementer
from zope.interface.interface import Interface
import socket


class Client(Interface):
    def connect(self):
        pass
    def sendall(self,message):
        pass
    def close(self):
        pass
    
#短链接，服务端派发了zookeeper事件，由客户端监听者接受到信息后，才会创建短链接从服务器获取信息或者数据
@implementer(Client)
class AbstractClient(object):
    def __init__(self,ip=ConfigHolder.getConfig().getProperty(BASE, SERVER_IP),port=int(ConfigHolder.getConfig().getProperty(BASE, SERVER_PORT))):
        self.ip=ip
        self.port=port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self):
        server_address = (self.ip, self.port)
        self.sock.connect(server_address)
        
    def sendall(self,message):
        self.sock.sendall(MessageCodec().encode(message))
        doRequestHandle(self.sock)
        
class SocketClient(AbstractClient):
    pass
        
        
        