#-*- coding: UTF-8 -*- 
'''
Created on 2016年2月3日

@author: huawei
'''
from abstract_parse import AbstractParse
from bs4 import BeautifulSoup
from crawler import TaobaoCrawler
#htps://detail.tmall.com/item.htm?id=45802761302
#http://item.taobao.com/item.htm?id=45802761302
class Tmall(AbstractParse):
        crawler= TaobaoCrawler() 

        def parse(self, html):
            shop_name=''
            shop_url=''
            company_name=''
            phone=''
            location = ''
            province =''
            city = ''
            html= html.decode('gbk').encode("utf-8")
#             print(html)
            soup = BeautifulSoup(html, "html.parser")
            
            if html.find("很抱歉，您查看的商品找不到了") >0:
                return (shop_name, shop_url, company_name, phone, province, city)
                
            shop_link = soup.find_all('a', class_='slogo-shopname')[0]
#             print shop_link
             
            shop_name = shop_link.find('strong').get_text()
            shop_url = 'http:' + shop_link['href']
            
            
            
            url = soup.find('input', {'id': 'dsr-ratelink'}).get('value')
#             print url
            
         
            detail_html = Tmall.crawler.do_get("http:"+url)
            
            
            soup = self.get_beautiful_soup(detail_html)
            company =  soup.find_all('li', class_='company')
            if company :
                company_name =  company[0].find("div",class_="fleft2").get_text()
                company_name =  company_name.strip()
                city = company[0].find_next("li").find_next("li").get_text()
                city = city.strip().replace("所在地区：", "")
                phone = company[0].find_next("li").find_next("li").find_next("li").get_text()
                if phone.find("服务电话") > -1:
                    phone = phone.strip().replace("服务电话：","")
                else:
                    phone =""
                
            
#             candidate = soup.find_all('li', class_='shopkeeper')[0].find_next_siblings()
# #             
#             company_name = candidate[1].find('div').get_text().strip()
#             
#             if(u'年店' in company_name):
#                 company_name = candidate[2].find('div').get_text().strip()
#             
#             location = soup.select('.locus')[0].find('div').get_text().strip()
#             
#             if(location != None and location!= ''):
#                 location = location.split(',')
#                 province = location[0].strip()
#                 city = location[1].strip()
            
#             print shop_name, shop_url, company_name, phone, province, city
#             company_name = company_name if company_name else ""
#             phone = phone if phone else ""
#             province = province if province else ""
#             city = city if city else ""
            return (shop_name, shop_url, company_name, phone, province, city)
            
            
        
        

        
        
        
