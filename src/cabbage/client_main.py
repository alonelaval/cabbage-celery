# -*- encoding: utf-8 -*-
'''
Created on 2016年6月13日

@author: hua
'''

from cabbage.constants import CFG_PATH
import os

if __name__=="__main__":
    os.environ.setdefault(CFG_PATH, "")
    from cabbage.client_start import CabbageClientHolder
    CabbageClientHolder.getClient().start()
    
       
        
        
        