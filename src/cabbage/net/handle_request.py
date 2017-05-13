# -*- encoding: utf-8 -*-
'''
Created on 2016年6月7日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.common.serialize.serialize_holder import \
    SERIALEZE_HOLDER
from cabbage.message.message_codec import MessageCodec, HEAD_LEN
from cabbage.message.message_holder import MESSAGE_HOLDER

RECV_LEN= 4096
log = Logger.getLogger(__name__)

def doRequestHandle(sock):
    head = sock.recv(HEAD_LEN)
    if len(head) <HEAD_LEN:
        while len(head) <HEAD_LEN:
            l = HEAD_LEN - len(head)
            head += sock.recv(l)
    codec = MessageCodec()
    codec.decode(head)
    bodyLen = codec.messageLength
    body = None
    if bodyLen > RECV_LEN:
        body = sock.recv(RECV_LEN)
        while len(body)< bodyLen:
            body += sock.recv(RECV_LEN)
    else:
        body = sock.recv(bodyLen)
    
    msgObj = MESSAGE_HOLDER[codec.messageId]
    data = SERIALEZE_HOLDER[codec.serialize](msgObj).deserialize(body)
    msgInstance = msgObj(data)
    return msgInstance.doAction()
            
def handleRequest(conn,addr):
    try:
        resultMessage = doRequestHandle(conn) #msgInstance.doAction()
        #result一般为message类型
        if resultMessage:
            conn.sendall(MessageCodec().encode(resultMessage))
    except Exception:
        Logger.exception( log)
            
        
