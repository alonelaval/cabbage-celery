# coding: utf8
'''
Created on 2016-8-1

@author: yan.feng
'''

from cabbage.cabbage_celery.task import CabbageTask
from cabbage.common.log.logger import Logger
# from domain import exec_primarydomain

# from amazon_parse import Amazon
# from dangdang_parse import DangDang
# from suning_parse import Suning
# from yhd_parse import Yhd
# from jd_parse import Jd
# from taobao_parse import Taobao
# from tmall_parse import Tmall


from cabbage.utils.host_name import getHostName
from selenium import webdriver
import datetime
import json
import logging
import string
import time
import traceback
import urllib
import urlparse
import websocket
from product_detail_parser import ProductDetailParser

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

log = Logger.getLogger(__name__)

serverAddr = '10.0.137.88:8888'

productDetailParser = ProductDetailParser()

'''
      产品列表爬虫
'''
class ProductListCrawler:
    
    def __init__(self, lid):
        self.__initByLid(lid)
        self.productCount = 0
    
    '''
                    由Job表ID初始化
    '''
    def __initByLid(self, lid):
        self.lid = lid
        websocket.enableTrace(False)
        wsPath = "ws://%s/shop/ws" % serverAddr
        self.ws = websocket.create_connection(wsPath)
        try:
            param = {'method':'getJob', 'data':{'lid':lid}}
            msg = json.dumps(param)
            self.ws.send(msg)
            result = self.ws.recv()
            jsonData = json.loads(result)
            if jsonData['success']:
                self.shopId = jsonData['data']['shopId']
                self.shopName = jsonData['data']['shopName']
                self.platform = str(jsonData['data']['platform'])
                self.sid = jsonData['data']['sid']
                self.url = jsonData['data']['url']
                self.jobType = jsonData['data']['jobType']
                self.shopUpdated = True
        except Exception:
            # traceback.print_exc()
            log.exception(getHostName())
                    
    
    
    def getSearchUrl(self):
        links = self.infoBrowser.find_elements_by_tag_name('a')
        for link in links:
            href = link.get_attribute('href')
            if href is not None and href.endswith('search.htm?search=y'):
                return href
        return ''

    '''
                    解析url参数
    '''
    def __getParameterMap(self, url):
        query = urlparse.urlparse(url).query
        return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])
    
    '''
                    返回url根路径
    '''
    def __getHostUrl(self):
        curl = self.infoBrowser.current_url
        curl = str(curl)
        proto, rest = urllib.splittype(curl)
        host, rest = urllib.splithost(rest)
        hostUrl = '%s://%s' % (proto, host)
        return hostUrl
    
    '''
                    初始化数据结果集
    '''
    def __initDataMap(self):
        info = {}
        info['shopId'] = self.shopId
        info['shopName'] = self.shopName
        info['platform'] = self.platform
        info['sid'] = self.sid
        info['pName'] = None
        info['url'] = None
        info['productId'] = None
        info['salePrice'] = None
        info['totalSaleQuantity'] = None
        info['comment'] = None
        info['quantity'] = None
        info['colorCategory'] = None
        info['monthSaleQuantity'] = None
        info['brandId'] = None
        info['bcType'] = None
        info['createTime'] = None
        info['favcount'] = None
        info['deliveryLocation'] = None
        info['brandName'] = None
        info['styleId'] = None
        info['openTime'] = None
        info['descGap'] = None
        info['serviceGap'] = None
        info['logisticsGap'] = None
        info['picUrl'] = None
        info['size'] = None
        info['followCount'] = None
        return info
    
    '''
                   提取网页字段
    '''
#     def __handleEachItem(self, item):
#         subItems = item.find_elements_by_class_name('item')
#         lst = []
#         for sub in subItems:
#             info = self.__initDataMap()
#             try:
#                 arg = sub.find_element_by_css_selector('.detail a')
#                 if arg is not None:
#                     info['pName'] = arg.text
#                     href = arg.get_attribute('href')
#                     info['url'] = href
#                     pmap = self.__getParameterMap(info['url'])
#                     info['productId'] = int(pmap['id'])
#             except:
#                 pass
#             if info['productId'] is None or info['pName'] is None:
#                 continue
#             try:
#                 arg = sub.find_element_by_css_selector('.c-price')
#                 if arg is not None:
#                     info['salePrice'] = string.atof(arg.text) * 100
#             except:
#                 pass
#             lst.append(info)
#         return lst
    
    '''
                判断重复抓取
    '''
    def __checkIsCrawledDaily(self):
        try:
            param = {'method':'getShop', 'data':{'shopId':self.shopId}}
            self.ws.send(json.dumps(param))
            result = self.ws.recv()
            jsonData = json.loads(result)
            if bool(jsonData['success']):
                t = jsonData['data']['lastFetchProductTime']
                if t is not None:
                    left = datetime.datetime.now().strftime("%Y%m%d")
                    dt = time.strptime(t, "%Y-%m-%d %H:%M:%S")
                    y, m, d = dt[0:3]
                    right = datetime.datetime(y, m, d).strftime("%Y%m%d")
                    return right == left
        except Exception:
            # traceback.print_exc()
            log.exception(getHostName())
        return False
    
    '''
                入口方法,开始爬取
    '''
    def enter(self):
        start = time.clock()
        if int(self.jobType) == 1000 and not self.__checkIsCrawledDaily():
            self.mark(2)
            try:
                self.infoBrowser = webdriver.PhantomJS()
                self.__tryAndGet(self.url)
                hostUrl = self.__getHostUrl()
                if 'store.taobao.com' in hostUrl:
                    self.setInvalid(1)
                else: 
                    pages = self.getShopPages(self.url, str(self.platform),self.infoBrowser)
                    if pages:
                        isUpdateShop=True
                        pageCount,pageDetails= pages 
                        for pageNum,pageUrl in enumerate(pageDetails):
                            print  ('%s : SearchUrl: %s' % (getHostName(),pageUrl))
                            productIds = self.getProductIdsByPageUrl(pageUrl, self.platform,self.infoBrowser)
                            
                            try:
                                param = {'method':'updateShopPageState', 'data':{'shopId': self.shopId, 'pageState':pageNum + 1}}
                                self.ws.send(json.dumps(param))
                                self.ws.recv()
                            except Exception:
                                log.exception(getHostName())
                            
                            nLst = []
                            for productId in productIds:
                                info = self.__initDataMap()
                                url = "https://item.taobao.com/item.htm?id=%s"%productId
                                info['url']=url
                                nData = self.__complementData(info)
                                
                                if isUpdateShop:
                                    self.__updateShop(info)
                                    isUpdateShop = True
                                
                                if nData is not None:
                                    nLst.append(nData)
                                    
                           
                            self.productCount = self.productCount + len(nLst)
                            
                            self.saveToDB(nLst)
            
#                     self.platform = 'taobao' if 'taobao' in hostUrl else 'tmall'
#                     searchUrl = hostUrl + '/search.htm?search=y'
#                     print  ('%s : SearchUrl: %s' % (getHostName(),searchUrl))
#                     self.__loop(searchUrl)
            

                    self.__addShopProductSearchListByJobId()
                    self.setInvalid(0)
            except Exception:
                log.exception(getHostName())
            self.mark(1)
            self.close()
        print ('%s: shopId:%s  Run completed. Take(sec): %d. ProductCount: %d' % (getHostName(), self.shopId , time.clock() - start, self.productCount))
    
    '''
                    设置网店失效
    '''
    def setInvalid(self,flag):
        try:
            param = {'method':'storeInvalid', 'data': {'shopId':self.shopId,'flag': flag}}
            self.ws.send(json.dumps(param))
            result = self.ws.recv()
            print '%s :  shopId:%s  mark shop : %s' % (getHostName(), self.shopId, result)
        except Exception:
            log.exception(getHostName())
    
    '''
                    标记任务状态
    '''
    def mark(self, flag):
        try:
            param = {'method':'updateShopRunState', 'data': {'shopId':self.shopId, 'flag':flag}}
            self.ws.send(json.dumps(param))
            result = self.ws.recv()
            print '%s :  shopId:%s  Mark result: %s' % (getHostName(), self.shopId, result)
        except Exception:
            log.exception(getHostName())
            # traceback.print_exc()
    
    '''
                    尝试请求,请求最大次数3次
    '''
    def __tryAndGet(self, url):
        i = 0
        while i < 3:
            try:
                self.infoBrowser.get(url)
                self.infoBrowser.implicitly_wait(45)
                self.infoBrowser.current_window_handle
                break
            except Exception:
                log.exception(getHostName())
                # traceback.print_exc()
            i += 1
        
    '''
                  循环爬取并分页
    '''
#     def __loop(self, url):
#         print  ('%s : Fetch url: %s' % (getHostName(),url))
# 
#         self.__tryAndGet(url)
#         
#         currentPageState = None
#         try:
#             if self.platform is 'taobao' :
#                 pages = self.infoBrowser.find_element_by_class_name('page-info')
#                 if pages is not None:
#                     currentPageState = pages.text
#             else:
#                 pages = self.infoBrowser.find_element_by_class_name('ui-page-s-len')
#                 if pages is not None:
#                     currentPageState = pages.text
#         except Exception:
#             log.exception(getHostName())
#             print '%s : Cannot find page state string'% getHostName()
#                 
#         if currentPageState is not None:
#             try:
#                 param = {'method':'updateShopPageState', 'data':{'shopId': self.shopId, 'pageState':currentPageState}}
#                 self.ws.send(json.dumps(param))
#                 self.ws.recv()
#             except Exception:
#                 log.exception(getHostName())
#                 # traceback.print_exc()
#             
#         self.__loadData()
#         
#         pageItem = self.infoBrowser.find_element_by_class_name('pagination')
#         if pageItem is not None:
#             nextItem = pageItem.find_element_by_link_text(u'下一页')
#             if nextItem is None:
#                 nextItem = pageItem.find_element_by_css_selector('a[class="J_SearchAsync next"]')
#             if nextItem is not None:
#                 href = nextItem.get_attribute('href')
#                 if href is not None and href.strip() != '':
#                     self.__loop(href)
    

            
    def getShopPages(self, url, platform,infoBrowser):
        searchUrl = url + '/search.htm?search=y'
    #     print searchUrl
    #     if not hasattr(self, "infoBrowser"):
    #             self.infoBrowser = webdriver.PhantomJS()
        infoBrowser.get(searchUrl)
        infoBrowser.implicitly_wait(30)
        infoBrowser.current_window_handle
        infoBrowser.page_source
        time.sleep(1)
        if platform == 'taobao' :
            if infoBrowser.page_source.find("no-result-new") >0  or infoBrowser.page_source.find("图片轮播") > 0:
                return None
            try:
                pageItem =infoBrowser.find_element_by_class_name('pagination')
            except Exception:
                return (1, [searchUrl])
            
            if  pageItem is not None:
                pages = pageItem.find_element_by_class_name(u'page-info')
                pageUrl = pageItem.find_element_by_link_text(u'下一页').get_attribute('href')
                pageCount = int(pages.text.split("/")[1])
                if pageCount > 1:
                    return (pageCount, [self.repalcePageNo(pageUrl, i) for i in range(1, pageCount + 1)])
                else:
                    return (1, [searchUrl])
                
        if  platform == 'tmall':
            
            if infoBrowser.page_source.find("no-result-new") >0 or infoBrowser.page_source.find("图片轮播") > 0:
                return None
    #         try:
            pageItem = infoBrowser.find_element_by_class_name('ui-page-s')
    #         except:
    #             pass
            
            if  pageItem is not None:
                pages = pageItem.find_element_by_class_name(u'ui-page-s-len')
                pageUrl = pageItem.find_element_by_class_name(u'ui-page-s-next').get_attribute('href')
    #             print pageUrl
                pageCount = int(pages.text.split("/")[1])
                if pageCount > 1:
                    return (pageCount, [self.repalcePageNo(pageUrl, i) for i in range(1, pageCount + 1)])
                else:
                    return (1, [searchUrl])
        
        return None
    
    def getProductIdsByPageUrl(self, url, platform,infoBrowser):
        searchUrl = url 
#         infoBrowser = webdriver.PhantomJS()
        infoBrowser.get(searchUrl)
        infoBrowser.implicitly_wait(50)
        infoBrowser.current_window_handle
        infoBrowser.page_source
        time.sleep(1)
        if platform == 'taobao' :
            productItems = infoBrowser.find_elements_by_class_name('item')
    #         print len(productItems)
    #         if len(productItems) >0:  #避免抓取不到
    #             print productItems[0].text
        
            if len(productItems)==0:
                return None
            
            if productItems[0].get_attribute('data-id') is None:
    #             print "sleep"
                time.sleep(10)
                productItems = infoBrowser.find_elements_by_class_name('item')
                
            if productItems:
                return [i.get_attribute('data-id')  for i in productItems  if i.get_attribute('data-id') is not None]
            
        if platform == 'tmall' :
    
            J_TItems = infoBrowser.find_element_by_class_name(u'J_TItems')
             
            items = J_TItems.find_elements_by_xpath("div")
            pros = []
            for div in items:
                className = div.get_attribute("class") 
                if className == 'pagination':
                    break
                productItems = div.find_elements_by_class_name('item')
                if productItems[0].get_attribute('data-id') is None:
    #                 print "sleep"
                    time.sleep(10)
                    productItems = infoBrowser.find_elements_by_class_name('item')
                if productItems:
                    pros = pros + [i.get_attribute('data-id')  for i in productItems  if i.get_attribute('data-id') is not None]
            return pros
        return []
    def repalcePageNo(self, url, pageNo):
        bits = list(urlparse.urlparse(url))
        qs = urlparse.parse_qs(bits[4]) 
        qs["pageNo"] = pageNo
        bits[4] = urllib.urlencode(qs, True) 
        url = urlparse.urlunparse(bits)
        return url
    
    '''
                    更新网店信息部分字段
    '''
    def __updateShop(self, info):
        if self.shopUpdated:
            try:
                param = {'method':'updateShop', 'data':{'shopId':info['shopId'], 'descGap': info['descGap'], 'serviceGap': info['serviceGap'], \
                                                        'logisticsGap':info['logisticsGap'], 'picUrl':info['picUrl'], 'followCount':info['followCount'], \
                                                        'openTime': info['openTime']}}
                self.ws.send(json.dumps(param))
                res = self.ws.recv()
                jsonData = json.loads(res)
                if bool(jsonData['success']):
                    self.shopUpdated = bool(jsonData['result'])
            except Exception:
                log.exception(getHostName())
                # traceback.print_exc()
    
    '''
                        每页产品列表解析
    '''
#     def __loadData(self):
#         try:
#             items = self.infoBrowser.find_elements_by_css_selector('.J_TItems > div')
#             if not items:
#                 items = self.infoBrowser.find_elements_by_css_selector('div[class="shop-hesper-bd grid"] > div')
#             if not items:
#                 items = self.infoBrowser.find_elements_by_css_selector('div[class="skin-box-bd"] > div')
#             aLst = []
#             
#             for item in items:
#                 if item.get_attribute('class') == 'shop-filter':
#                     continue
#                 if item.get_attribute('class') == 'pagination' or item.get_attribute('class') == 'comboHd':
#                     break
#                 lst = self.__handleEachItem(item)
#                 if lst:
#                     aLst.extend(lst)
#             print  (getHostName() + ' : Each Page Products: %d' % len(aLst))
#             self.productCount += len(aLst)
#             
#             nLst = []
#             for info in aLst:
#                 nData = self.__complementData(info)
#                 if nData is not None:
#                     nLst.append(nData)
#             self.saveToDB(nLst)
#         except Exception:
#             log.exception(getHostName())
            # traceback.print_exc()
    
    def __addShopProductSearchListByJobId(self):
        msg = json.dumps({'method':'addShopProductSearchListByJobId', 'data':{'lid': self.lid}})
        self.ws.send(msg)
        result = self.ws.recv()
        jsonData = json.loads(result)
        if bool(jsonData['success']):
            print 'addShopProductSearchList ok.'
    
    '''
                根据产品ID远端查询产品详细信息,补全缺失信息
    '''
    def __complementData(self, info):
        data = productDetailParser.parse(info['url'])[2]
        if data is None:
            data = {'productId':info['productId'], 'valid':False}
        data['lid'] = self.lid
        return data
        
        
    '''
                    保存数据到DB
    '''
    def saveToDB(self, aLst):
        try:
            for info in aLst:
                msg = json.dumps({'method':'addProduct', 'data':info})
                self.ws.send(msg)
                result = self.ws.recv()
                jsonData = json.loads(result)
                if bool(jsonData['success']):
                    print '%s : Save product "%s" ok.' % (getHostName(),info['productId'])
        except Exception:
            log.exception(getHostName())
            # traceback.print_exc()
    
    '''
                    关闭
    '''
    def close(self):
        self.infoBrowser.quit()
        self.ws.close()


jd_domain='jd.com'
taobao_domain='taobao.com'
tmall_domain='tmall.com'
tmall_hk = 'tmall.hk'
suning_domain='suning.com'
yhd_domain='yhd.com'
dd_domain='dangdang.com'
z_domain="amazon.cn"
code="UTF-8"


# JD_OBJ=Jd()
# SUNING_OBJ =Suning()
# YHD_OBJ = Yhd()
# DANGDANG_OBJ =DangDang()
# AMAZON = Amazon()
# TAOBAO=Taobao()
# TMALL=Tmall()
# 
# parses={
# jd_domain:JD_OBJ,
# taobao_domain:TAOBAO,
# tmall_domain:Tmall,
# tmall_hk:Tmall,
# suning_domain:SUNING_OBJ,
# yhd_domain:YHD_OBJ,
# dd_domain:DANGDANG_OBJ,
# z_domain:AMAZON
# }

class ProductListCrawlerTask(CabbageTask):
    
#     def get_parse(self,shopUrl):
#         domain = exec_primarydomain(shopUrl)
#         if domain in parses:
#             return parses[domain]
#         else:
#             return None
        
        
        
    def doRun(self, *args, **kwargs):
        self.lid = kwargs['lid']
        if self.lid:
            crawler = ProductListCrawler(self.lid)
            crawler.enter()
            
    
            
        
if __name__ == '__main__':

    # url = 'https://shop110683172.taobao.com'
    # url = 'https://shop130207011.taobao.com'
    task = ProductListCrawlerTask()
    task.run(lid=1)
    # url = 'https://shop110683172.taobao.com'
    #     url = 'https://zhixingsm.tmall.com'
    # url = 'https://shop35219619.taobao.com/search.htm'
#     fetcher = ProductListCrawler(lid=173)
#     pages =  fetcher.getShopPages("http://shop34690320.taobao.com", 'taobao')
#     pageCount,pageDetails= pages 
#     print pageCount
#      
#     for pageUrl in pageDetails:
#         print pageUrl
#         productIds = fetcher.getProductIdsByPageUrl(pageUrl, 'taobao')
#         print productIds
#         print len(productIds)
#         break
        
        
