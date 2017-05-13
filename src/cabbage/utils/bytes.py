# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: huawei
'''

def bytes2int(s):
    return int(s.encode('hex'), 16)

def bytes2hex(s):
    return '0x'+s.encode('hex')

def int2bytes(i):
    h = int2hex(i)
    return hex2bytes(h)

def int2hex(i):
    return hex(i)
def int2BytesPack(i):
    import struct
    return struct.pack('>I', i)
def bytes2IntUnpack(bs):
    import struct
    return struct.unpack('>I', bs)
    
def hex2int(h):
    if len(h) > 1 and h[0:2] == '0x':
        h = h[2:]

    if len(h) % 2:
        h = "0" + h
    return int(h, 16)

def hex2bytes(h):
    if len(h) > 1 and h[0:2] == '0x':
        h = h[2:]

    if len(h) % 2:
        h = "0" + h
    return h.decode('hex')
