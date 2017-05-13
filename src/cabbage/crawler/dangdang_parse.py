#-*- coding: UTF-8 -*- 
'''
Created on 2016年2月15日

@author: huawei
'''
from abstract_parse import AbstractParse

class DangDang(AbstractParse):
    
    def getShop(self,html):
        soup = self.get_beautiful_soup(html,AbstractParse.HTML5_PARSER)
        shopName=None
        shopUrl = None
        
        if soup.find("div", class_="notfound_404_right"):#界面404
            return ("","","","") 
        
        legend_02 = soup.find('h1',class_='legend legend02')
        if legend_02 :
            span = legend_02.findAll('span')
            return  (span[1].getText(),'dangdang.com',"","") 
        
#        (shopCompany,shopPhone) = self.getcompanyinfo(html)
        legend =  soup.find('h1', class_='legend')
        if legend :
            a = legend.find("a")
            shopUrl = a['href']
            shopName =  a.getText()
            return  (shopName,shopUrl,"","")
            
        
        
        