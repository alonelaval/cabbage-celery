# -*- encoding: utf-8 -*-
'''
Created on 2016年2月3日

@author: hua
'''
from abstract_parse import AbstractParse
import chardet
from bs4 import BeautifulSoup

#htps://detail.tmall.com/item.htm?id=45802761302
#http://item.taobao.com/item.htm?id=45802761302
class Taobao(AbstractParse):
    def getShop(self,html):
        html_charset = ''
#         print html.decode('gbk').encode("utf-8")
        soup = BeautifulSoup(html)
        
        if html.find("很抱歉，您查看的宝贝不存在，可能已下架或者被转移")>0:
            return ("", "", '', '', "")
         
        shop_name = ''
        url = ''
        shipping_from = ''
        for script in soup.find_all('script'):
            script_text = script.get_text()
            if(self.is_script_g_config(script_text)):
                shop_name,url = self.get_info(script_text)
    
        soup.find_all('span', id='J-From')
        return (shop_name, url, '', '', shipping_from)
    
    def is_script_g_config(self, script_text):
        if('var g_config' in script_text):
            return True
        
    def get_info(self, script_text):
        shopname = ''
        url = ''
        for line in script_text.split('\n'):
            
            if('shopName' in line):
                shopname = self.extract_value(line).strip('\'').decode('unicode-escape')
            elif(line.strip().startswith('url')):
                url = self.extract_value(line).strip('\'').strip('/')

        return shopname, url
    
    def extract_value(self, line):
        value = line.split(':')[1].strip().strip(',')
        return value