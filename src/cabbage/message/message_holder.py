# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from cabbage.message.file_message import FileRequestMessage, \
    FileResponseMessage
from cabbage.message.message_ids import FILE_REQUEST_MSG, \
    FILE_RESPONSE_MSG
MESSAGE_HOLDER={
            FILE_REQUEST_MSG:FileRequestMessage,
            FILE_RESPONSE_MSG:FileResponseMessage
            }