# -*- encoding: utf-8 -*-
'''
Created on 2016年2月3日

@author: hua
'''
from abstract_parse import AbstractParse


class Yhd(AbstractParse):
    def getShop(self,html):
       
        soup = self.get_beautiful_soup(html,AbstractParse.HTML5_PARSER)
#        print html
        if soup.find("div", attrs={"id":"main404"}):#界面404
            return ("","","","")
        
        shopUrl =""
        shopName =""
        
        if soup.find("p",class_="shop_name clearfix"):
            a = soup.find("p",class_="shop_name clearfix").find("a")
            shopUrl= a['href']
            shopName = a.find("strong").getText()
        if soup.find("span",class_="deliver_name"): #国际店
            a = soup.find("span",class_="deliver_name").find("a")
            shopUrl= a['href']
            shopName = a.getText()
        
        html = self.get_index(shopUrl) #从首页抓取公司信息，一号店一般首页都有这种信息
#        f = open("./html","w")
#        f.write(html)
        
        if html.find("该页面已经被删除")>=0:
            return (shopName,shopUrl,"","")
           
        soup = self.get_beautiful_soup(html,AbstractParse.HTML5_PARSER)
        lis = soup.find("div",class_="shop-des").find("ul").find_all("li")
        if len(lis) ==0:
            return (shopName,shopUrl,"","")
        
        shopCompany = lis[0].find("span").getText()
        shopPhone=lis[2].find("span").getText()
        
        return (shopName,shopUrl,shopCompany,shopPhone)
        
        
    def get_index(self,url):
        return self.do_get(url)
    