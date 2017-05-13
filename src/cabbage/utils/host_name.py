# -*- encoding: utf-8 -*-
'''
Created on 2016年6月24日

@author: hua
'''
import socket
def getHostName():
    hostname=socket.gethostname()
    return hostname
HOST_NAME=getHostName()

def getLocalIp():
    try:
        ip =([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
        return ip
    except :
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("baidu.com",80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            pass
    return None

LOCAL_IP=getLocalIp()

# print getLocalIp()
# def getNetworkIp():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(('baidu.com', 80))
#     return s.getsockname()[0]
# 
# print getNetworkIp()
# import socket
# print([(s.connect(('114.114.114.114', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
# 
# 
# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("baidu.com",80))
# print s.getsockname()
# print(s.getsockname()[0])
# s.close()


# print socket.create_connection(("12.12.12.12", 80),timeout=3)
# print socket.gethostbyname("ubuntu")
# def get_ip_address(ifname): 
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#     return socket.inet_ntoa(fcntl.ioctl( 
#     s.fileno(), 
#     0x8915, # SIOCGIFADDR 
#     struct.pack('256s', ifname[:15])
#     )[20:24]) 
#  
# print get_ip_address('lo')#环回地址 
# print get_ip_address('eth0')#主机ip地址 
