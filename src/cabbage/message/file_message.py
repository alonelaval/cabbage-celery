# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from cabbage.constants import FILE_PATH, FILE_NAME, FILE_CONTENT, \
    JOB_ID, TYPE
from cabbage.message.base_message import AbstractMessage
from cabbage.message.message_ids import FILE_REQUEST_MSG, \
    FILE_RESPONSE_MSG

class FileRequestMessage(AbstractMessage):
    MAIN="main"
    ATTACH="attach"
    def __init__(self,data=None):
        self.messageId=FILE_REQUEST_MSG
        if data:
            self.data= data
#             self.filePath=data[FILE_PATH]
            self.fileName=data[FILE_NAME]
            self.jobId =data[JOB_ID]
            self.type = data[TYPE]
            
    def getAction(self):
        from cabbage.message.action.file_action import RequestFileAction
        return RequestFileAction(self)
    
class FileResponseMessage(AbstractMessage):
    def __init__(self,data=None):
        self.messageId= FILE_RESPONSE_MSG
        if data:
#             self.filePath=data[FILE_PATH]
            self.fileName=data[FILE_NAME]
            self.fileContent=data[FILE_CONTENT]
            self.jobId =data[JOB_ID]
        
    def getAction(self):
        from cabbage.message.action.file_action import ResponseFileAction
        return ResponseFileAction(self)
