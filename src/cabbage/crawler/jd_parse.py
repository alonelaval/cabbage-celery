# -*- encoding: utf-8 -*-
'''
Created on 2016年2月3日

@author: hua
'''
from abstract_parse import AbstractParse

class Jd(AbstractParse):
    title='京东(JD.COM)-综合网购首选-正品低价、品质保障、配送及时、轻松购物！'
    def getShop(self,html):
    
        soup = self.get_beautiful_soup(html)
        if soup.title.text ==Jd.title and html.find("<!--index_ok-->"):#网店不存在，直接跳到主页去了
            return ("","","","")
        
        if soup.find("div", class_="m-itemover-title"): #商品已下架
            return ("","","","")
        
        a = soup.find("div", class_="seller-infor").find("a")
        shopName = a.text
        shopUrl = a['href']
        shopCompany=soup.find("span",class_="text J-shop-name").text
        '''京东没有电话'''
        return (shopName,shopUrl,shopCompany,"")