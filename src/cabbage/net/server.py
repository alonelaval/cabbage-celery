# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from zope.interface.interface import Interface

class Server(Interface):
    
    def start(self):
        pass
    
#     def receive(self):
#         pass
    
#     def sendall(self,conn,message):
#         pass
    
    def connected(self):
        pass
        
    def stop(self):
        pass