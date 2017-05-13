'''
Created on 2016-8-31

@author: admin
'''
from cabbage.config import ConfigHolder
from cabbage.constants import BASE, LOG_CONFIG_PATH

if __name__ == '__main__':
    a = ConfigHolder.getConfig().getProperty(BASE,LOG_CONFIG_PATH)
    print a
    s = "\u4e0a\u6d77"
    print(s.decode('unicode-escape'))  
    pass