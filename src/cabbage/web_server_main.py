# -*- encoding: utf-8 -*-
'''
Created on 2016年6月8日
 
@author: hua
'''
from cabbage.constants import CFG_PATH
import os

if __name__=="__main__":
    os.environ.setdefault(CFG_PATH, "")
    from cabbage.web_server_start import CabbageWebServerHolder
    CabbageWebServerHolder.getServer().start()