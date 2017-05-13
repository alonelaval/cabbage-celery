# coding: utf8
'''
Created on 2016-9-1

@author: yan.feng
'''

import json
import re
import requests
import string
import urlparse

class ProductDetailParser:

    def __init__(self, **kargs):
        self.args = kargs
        pass
    
    def __getNumber(self, s):
        m = re.findall(r'\d+[.]?\d+', s)
        if m:
            return m[0]
        else:
            return None

    '''
                    初始化数据结果集
    '''
    def __initDataMap(self):
        info = {}
        info['lid'] = None
        info['shopId'] = None
        info['shopName'] = None
        info['sid'] = None
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
        info['platform'] = None
        info['followCount'] = None
        info['valid'] = True
        return info
    
    '''
                    设置其他字段
    '''
    def __setProps(self, jsonData, info):
        try:
            props = jsonData['data']['props']
            for a in props:
                if a['name'] == u'货号' or a['name'] == u'款号' or a['name'] == u'ISBN编号':
                    info['styleId'] = a['value']
                elif a['name'] == u'品牌':
                    info['brandName'] = a['value']
        except:
            pass
    
    '''
                    获取颜色分类
    '''
    def __setColorCats(self, jsonData, info):
        try:
            skuProps = jsonData['data']['skuModel']['skuProps']
            for cc in skuProps:
                if cc['propName'] == u'颜色分类' or cc['propName'] == u'颜色' or cc['propName'] == u'颜色种类':
                    arr = []
                    for col in cc['values']:
                        arr.append(col['name'])
                    info['colorCategory'] = ','.join(arr)
        except:
            pass
    
    '''
                   获取尺码
    '''
    def __setSize(self, jsonData, info):
        try:
            skuProps = jsonData['data']['skuModel']['skuProps']
            for cc in skuProps:
                if cc['propName'] == u'尺码' or cc['propName'] == u'尺寸':
                    arr = []
                    for col in cc['values']:
                        arr.append(col['name'])
                    info['size'] = ','.join(arr)
                    break
        except:
            pass
    
    '''
                    获取评价
    '''
    def __setGap(self, jsonData, info):
        try:
            evaluateInfo = jsonData['data']['seller']['evaluateInfo']
            for a in evaluateInfo:
                if a['name'] == u'描述相符':
                    info['descGap'] = a['highGap']
                elif a['name'] == u'服务态度':
                    info['serviceGap'] = a['highGap']
                elif a['name'] == u'物流服务':
                    info['logisticsGap'] = a['highGap']
        except:
            pass
    
    '''
                    获取销量/库存/发货地
    '''
    def __setQuantityData(self, jsonData, info):
        try:
            jsonStr = jsonData['data']['apiStack'][0]['value']
        except:
            return
        try:
            lst = re.findall('"totalSoldQuantity":"\d+"', jsonStr)
            totalSoldQuantity = lst[0]
            info['monthSaleQuantity'] = self.__getNumber(totalSoldQuantity)
        except:
            pass
        try:
            lst = re.findall('"quantity":"\d+"', jsonStr)
            quantity = lst[0]
            info['quantity'] = self.__getNumber(quantity)
        except:
            pass
        try:
            lst = re.findall('"price":"\d+[.]?\d+"', jsonStr)
            price = lst[0]
            info['salePrice'] = string.atof(str(self.__getNumber(price))) * 100  # 价格乘以100
        except:
            pass
        try:
            p = re.compile('[\\\\]+')
            otherJsonStr = re.sub(p, '', jsonStr)
            otherJsonStr = otherJsonStr.replace('"[', "[")
            otherJsonStr = otherJsonStr.replace(']"', "]")
            jsonObj = json.loads(otherJsonStr)
            info['monthSaleQuantity'] = jsonObj['data']['itemInfoModel']['totalSoldQuantity']
            info['quantity'] = jsonObj['data']['itemInfoModel']['quantity']
        except Exception:
            pass
    
    '''
                    解析URL参数
    '''
    def __getParameterMap(self, url):
        query = urlparse.urlparse(url).query
        return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])
    
    '''
                    解析产品URL,获取相关属性
    '''
    def parse(self, url):
        query = self.__getParameterMap(url.strip());
        if not query.has_key('id'):
            return (False, u"缺少商品ID", None)
        productId = query['id']
        serviceUrl = 'http://hws.m.taobao.com/cache/wdetail/5.0/?id=%s&ttid=2013@taobao_h5_1.0.0&exParams={}' % productId
        s = requests.session()
        try:
            r = s.get(serviceUrl, timeout=10)
            jsonData = r.json()
        except Exception:
            return (False, u"获取商品信息失败", None)
        s.close()
        
        try:
            ret = jsonData['ret'][0]
            if u'宝贝不存在' in ret:
                return (False, u"宝贝不存在", None)
        except Exception:
            raise
        
        info = self.__initDataMap()
        info['productId'] = productId
        info['url'] = url
        try:
            info['shopId'] = jsonData['data']['seller']['shopId']
        except:
            pass
        try:
            info['pName'] = jsonData['data']['itemInfoModel']['title']
        except:
            pass
        try:
            info['brandId'] = jsonData['data']['trackParams']['brandId']
        except:
            pass
        try:
            info['bcType'] = jsonData['data']['trackParams']['BC_type']
        except:
            pass
        try:
            info['favcount'] = jsonData['data']['itemInfoModel']['favcount']
        except:
            pass
        try:
            info['picUrl'] = jsonData['data']['seller']['picUrl']
        except:
            pass
        try:
            info['openTime'] = jsonData['data']['seller']['starts']
        except:
            pass
        try:
            info['followCount'] = jsonData['data']['seller']['fansCount']
        except:
            pass
        try:
            info['comment'] = jsonData['data']['rateInfo']['rateCounts']
        except:
            pass
        try:
            info['deliveryLocation'] = jsonData['data']['itemInfoModel']['location']
        except:
            pass
        
        self.__setProps(jsonData, info)
        self.__setColorCats(jsonData, info)
        self.__setQuantityData(jsonData, info)
        self.__setGap(jsonData, info)
        self.__setSize(jsonData, info)
        
        return (True, None , info)

if __name__ == '__main__':
    pass