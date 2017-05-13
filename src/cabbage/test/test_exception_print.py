# -*- encoding: utf-8 -*-
'''
Created on 2016年8月17日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.utils.host_name import getHostName
def error():
    raise  Exception("dadsfasdf")

log = Logger.getLogger(__name__)
try:
    error()
except Exception as e:
    log.exception(getHostName())
