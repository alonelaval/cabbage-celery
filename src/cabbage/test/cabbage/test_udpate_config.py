# -*- encoding: utf-8 -*-
'''
Created on 2016年8月31日

@author: huawei
'''
from cabbage.utils.imports import find_module


result = find_module("cabbage.test.cabbage.cabbage_celeryconfig")
f = open(result[1],"a+")
f.write("a=a\r")
print f.read()
f.close()
