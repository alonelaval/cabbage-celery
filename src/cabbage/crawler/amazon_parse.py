#-*- coding: UTF-8 -*- 
'''
Created on 2016年2月15日

@author: huawei
'''
from abstract_parse import AbstractParse
class Amazon(AbstractParse):
    URL = 'http://www.amazon.cn/'
    #http://www.amazon.cn/gp/product/B00NWLNVFA/ 直接能获取到网店首页
    #http://www.amazon.cn/gp/product/B00W159WEW/ 需要绕弯
    #http://www.amazon.cn/gp/product/B0095N9FFE/ 404
    #http://www.amazon.cn/gp/product/B00C9UVOA4/  http://www.amazon.cn/gp/product/B00GLPZCME/  没有找到任何与相关的商品
    #http://www.amazon.cn/gp/product/B00JWG9MWU/  您是否找到了要查找的商品？
    def getShop(self,html):
        soup = self.get_beautiful_soup(html,AbstractParse.HTML5_PARSER)
        shopName=None
        shopUrl = None
        
        span = soup.find("span",attrs={'id':'ddmMerchantMessage'})
        if span : #直接获取
            a = span.find("a")
            herf = a['href']
#            shopName = a.getText()
            return self.get_shop_info(Amazon.URL+herf)
        
        brand = soup.find("a",attrs={'id':'brand'})
        if brand : #获取商标
            herf =  brand['href']
            return self.get_shop(Amazon.URL+herf)
            
         
        return  ("","","","")
        
        
    def get_shop(self,url):
        html = self.do_get(url)
        soup = self.get_beautiful_soup(html,AbstractParse.HTML5_PARSER)
        if html.find("没有找到任何与") >0:
            return ("","","","")
        a = soup.find("a",class_='a-link-normal a-color-base a-text-bold')
        if a:
            shop_name=a.getText()
            
            herf = a['href']
            html = self.do_get(Amazon.URL+herf)
            soup = self.get_beautiful_soup(html,AbstractParse.HTML5_PARSER)
            
            li = soup.findAll("a",class_="a-link-normal s-access-detail-page  a-text-normal")
            
            if li and len(li)>0:
                for a in li:
                    href = a['href']
                    html = self.do_get(href)
                    soup = self.get_beautiful_soup(html,AbstractParse.HTML5_PARSER)
                    span = soup.find("span",attrs={'id':'ddmMerchantMessage'})
                    if span : #直接获取
                        a = span.find("a")
                        herf = a['href']
                        (shop_name,shop_url,shop_company,shop_phone) = self.get_shop_info(Amazon.URL+herf)
                        if shop_name != "":
                            return (shop_name,shop_url,shop_company,shop_phone)
                        else:
                            continue
                
            return  ("","","","")
        else :
            
            
            li = soup.findAll("a",class_="a-link-normal s-access-detail-page  a-text-normal")
            
            if li and len(li)>0:
                for a in li:
                    href = a['href']
                    html = self.do_get(href)
                    soup = self.get_beautiful_soup(html,AbstractParse.HTML5_PARSER)
                    span = soup.find("span",attrs={'id':'ddmMerchantMessage'})
                    if span : #直接获取
                        a = span.find("a")
                        herf = a['href']
                        (shop_name,shop_url,shop_company,shop_phone) = self.get_shop_info(Amazon.URL+herf)
                        if shop_name != "":
                            return (shop_name,shop_url,shop_company,shop_phone)
                        else:
                            continue
            
            
            return ("","","","")
          
    
    def get_shop_info(self,url):
        html = self.do_get(url)
        soup = self.get_beautiful_soup(html,AbstractParse.HTML5_PARSER)
        if not soup.find("li",class_="aag_storefront"):
            return ("","","","")
        
        shop_url = soup.find("li",class_="aag_storefront").find('a')['href']
        shop_name= soup.find("li",class_="aag_storefront").find('a').getText().strip().replace("店铺","")
        ul =  soup.find("ul",class_="aagLegalData")
        shop_company =  ul.findAll("li")[0].getText().split(":")[1]
        shop_phone = ul.findAll("li")[1].getText().split(":")[1]
        return (shop_name,shop_url.strip(),shop_company.strip(),shop_phone.strip())
        
            
    
        