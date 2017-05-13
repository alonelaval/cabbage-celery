#coding=utf-8
'''
Created on 2014年2月15日

@author: xuji
'''


import os
import platform
import random
import sys
import tempfile
import threading

import chardet


#为避免在Daemon进程中相对路径取出不正确，必须在导入模块时获得当前路径
__PWD = os.path.abspath(os.path.dirname(sys.argv[0]))

#实现singleton模式
def singleton(cls,*args,**kwargs):
    instances = {}
    def getInstance(*args,**kwargs):
        lock = threading.Lock()
        if cls not in instances:
            lock.acquire()
            if cls not in instances:
                instances[cls] = cls(*args,**kwargs)
            lock.release()
        return instances[cls]
    return getInstance

def pwd():
    return __PWD

def get_encoding(text):
    '''
        判断字符编码，结果可能不准确
    '''
    if isinstance(text, unicode):
        return unicode.__name__
    
    try:
        return chardet.detect(text)[1]
    except:
        return 'utf-8'

def encode(text, charset):
    '''
        将字符串编码为指定的字符集
    '''
    coding = get_encoding(text)
    return text.decode(coding).encode(charset)

def get_tempfile(suffix, prefix):
    return tempfile.mktemp(suffix, prefix)
    
def get_temppath(prefix):
    return tempfile.mkdtemp('', prefix)

def is_windows():
    return platform.system().lower() == 'windows'

if __name__ == '__main__':

    print chardet.detect('abd124535235@343534')
    print isinstance('上海', unicode)
    
    #s = '测试'
    #print chardet.detect(s.decode('utf-8').encode('gbk'))
