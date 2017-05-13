# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from gevent import socket
from gevent.pool import Pool
from gevent.server import StreamServer
import gevent
urls = ['www.google.com', 'www.example.com', 'www.python.org']
jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
gevent.joinall(jobs, timeout=2)
for job in jobs:
    print job.value
    
    
 
def handle(socket, address):
        print('new connection!')

pool=Pool(111)
server = StreamServer(('127.0.0.1', 1234),handle,spawn=pool) # creates a new server
server.serve_forever() # start accepting new connections