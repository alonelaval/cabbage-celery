# -*- encoding: utf-8 -*-
'''
Created on 2016年8月22日

@author: hua
'''
class JsonResult(object):
    RESULT_SUCCESS = 0
    RESULT_NOT_AUTH = 1
    RESULT_NO_DATA = 2
    RESULT_REQUEST_EXPIRE = 4
    RESULT_PARAM_ERROR = 5
    RESULT_UNKNOWN_ERROR = 99999
    def __init__(self,result=None,message=None,data=None):
        self.result= result
        self.message=message
        self.data=data
    
    def asDict(self):
        return {"result":self.result,"message":self.message,"data":self.data}
        
        