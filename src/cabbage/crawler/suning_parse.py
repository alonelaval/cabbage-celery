# -*- encoding: utf-8 -*-
'''
Created on 2016年2月3日

@author: hua
'''
from abstract_parse import AbstractParse
from bs4 import BeautifulSoup
import re

class Suning(AbstractParse):
    
    def getShop(self,html):
        soup = self.get_beautiful_soup(html,AbstractParse.HTML5_PARSER)
        shopName=None
        shopUrl = None
        for t in soup.findAll('div',class_="breadcrumb"): #获取首页和网店名称
            for i,a in enumerate(t.findAll("a")):
                if i ==1 :
                    shopName =  a.text
                    shopUrl = a['href']
        
        if html.find("店铺装修中")>0:
            return (shopName,shopUrl,"","")
        
        
#        (shopCompany,shopPhone) = self.getcompanyinfo(html)
        spans =  soup.findAll('span', 'detail-val')
        shopCompany = spans[0].getText()
        shopPhone = ""
        if len(spans) >1:
            shopPhone = spans[1].getText()
        return (shopName.strip(),shopUrl,shopCompany,shopPhone)
    
    
#    def getcompanyinfo(self,htmlContent):
#        '''
#                        提取公司名称和公司电话
#        '''
#        companyName = None
#        companyTel = None
#        if not htmlContent:
#            return (companyName, companyTel)
#        isDetailDiv = False
#        for templine in htmlContent.split("\n"):
#            templine = templine.strip()
#            if len(templine) == 0:
#                continue
#            if re.match(r'.*?<div\s*class=.{1}si-detail.{1}>', templine.strip()):
#                isDetailDiv = True
#                continue
#            match = re.match(r'.*?公司：</span><span\s+class=.{1}detail-val.{1}>(.*)</span>', templine)
#            if match and isDetailDiv:
#                companyName = match.group(1)
#                continue
#            match = re.match(r'.*?TEL：.*?<span\s+class=.{1}detail-val.{1}>.*?(.+).*?</span>', templine)
#            if match and isDetailDiv:
#                companyTel = match.group(1).strip()
#                break
#        return (companyName, companyTel)