# -*- encoding: utf-8 -*-
'''
Created on 2016年2月3日

@author: hua
'''
from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
import requests
import urllib2

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'

HEADERS = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "User-Agent":  USER_AGENT}

TIMEOUT = 60

class AbstractParse(object):
    __metaclass_ = ABCMeta
    HTML5_PARSER="html5lib"
    
    @abstractmethod
    def getShop(self,url):
        '''
            返回网店信息
        '''
        pass
    
    @abstractmethod
    def getProducts(self,url):
        '''返回产品信息'''
        pass
    
    
    @abstractmethod
    def getProduct(self,url):
        pass
    
    def get_beautiful_soup(self,html,parser="html.parser"):
        try:
            return  BeautifulSoup(html, parser) 
        except Exception:
            return BeautifulSoup(html, AbstractParse.HTML5_PARSER) 
        
    def do_get(self, url, headers=HEADERS):
        '''
        execute http get method
        '''
        response = None
        try:
            return requests.get(url,headers=headers).content
        finally:
            if response:
                response.close()