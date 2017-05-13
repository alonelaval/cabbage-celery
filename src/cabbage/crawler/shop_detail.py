# -*- coding: UTF-8 -*- 
'''
Created on 2016年6月20日

@author: huawei
'''

from bs4 import BeautifulSoup
from requests.exceptions import  RequestException
from requests.packages import urllib3
from urllib import unquote
import time
import traceback
from cabbage.crawler.crawler import TaobaoCrawler
urllib3.disable_warnings()

taobao = TaobaoCrawler()
no_result = "error-notice"
TIME_FORMAT = "%Y-%m-%d"
NULL = None

def areaGet(provcity):
    if provcity == "":
        return "", ""
    if provcity == NULL:
        return None, None
    if provcity.find(","):
        area = str(provcity).strip().split(",")
        if len(area) > 1:
            return area[0].strip(), area[1].strip()
        else:
            return area[0].strip(), area[0].strip()
    else:
        area = str(provcity).strip().split(" ")
        if len(area) > 1:
            return area[0].strip(), area[1].strip()
        else:
            return area[0].strip(), area[0].strip()

'''isTmall,userId,shopId,nickName,shopName,shopUrl,openTime,rateRankUrl,category,area,charge,isCompany,companyName'''

'''userId,shopId,shopName,shopUrl,companyName,companyCode,category,area,type,platform'''

def findShop(url):
    html = getHtml(url)
    soup = BeautifulSoup(html, "html.parser")
    if html.find(no_result) > 0:
        return None
    
    title = soup.title.string
    if title.find("淘宝网") > 0:
        return getTaobaoData(soup, url)
    else:
        return getTmallData(soup)
        
    
        
def getTaobaoData(soup, url):
    
    scriptData = getTaobaoScriptData(soup)
  
    if scriptData:
#         data  = getUserId_shopId_userNick(scriptData)
        userId, shopId, nickName = scriptData
        nickName = unquote(str(nickName))
    else:
        return None
    isCompany = False
    companyName = NULL
    shopName = NULL
    shopUrl = url
    idTime = NULL
    if soup.find("span", class_="shop-name") is None:
        
        if soup.find("a", class_="shop-name-link"):
            shopName = soup.find("a", class_="shop-name-link").getText()
            shopUrl = soup.find("a", class_="shop-name-link").get('href')
            shopUrl = shopUrl[2:len(shopUrl)]
            companyName = soup.find("span", class_="company-name").getText() if soup.find("span", class_="company-name") else NULL
            isCompany = True if soup.find("span", class_="company-name") else False
        if soup.find("span", class_="shop-rank"):
            rateRankUrl = soup.find("span", class_="shop-rank").find("a").get('href')
        else:
            rateRankUrl = soup.find("div", class_="shop-dynamic-score").find("a", class_="J_TGoldlog").get('href')
        reg_age = NULL
        
        if soup.find("li", class_="setuptime"):
            setuptime = soup.find("li", class_="setuptime").getText()
            setuptime = setuptime.split("：")[1].strip()
            reg_age = setuptime
#             now =  datetime.datetime.now()
#             agoDate = datetime.datetime.strptime(setuptime,TIME_FORMAT)
#             reg_age=  (now - agoDate).days/365
        
        if idTime == NULL and  soup.find("span", class_="id-time"):
            idTime = soup.find("span", class_="id-time").getText()
            
        (category, area, charge) = getTaobaoRate(rateRankUrl)
        if area:
            area = area.replace("\t", "")
            area = area.replace(" ", "")
        area = area if area != '' else NULL
        area = area if area != '' else NULL
        charge = charge.replace(",", "") if charge != NULL else NULL
        shopName = shopName if shopName != NULL else nickName
        rateRankUrl = rateRankUrl[2:len(rateRankUrl)]
        return (False, userId, shopId, nickName, shopName, shopUrl, reg_age, idTime, rateRankUrl, category, area, charge, companyName, isCompany)
       
    
    shopData = soup.find("span", class_="shop-name").find("a", class_="J_TGoldlog")
    shopName = shopData.getText().replace("进入店铺", "")
    shopUrl = shopData.get('href')
    shopUrl = shopUrl[2:len(shopUrl)]
    
    openTime = soup.find("span", class_="open-time")
    openTime = openTime.getText().strip() if  openTime else NULL
    
    if idTime == NULL and  soup.find("span", class_="id-time"):
        idTime = soup.find("span", class_="id-time").getText()
    rateRankUrl = soup.find("span", class_="shop-rank").find("a").get('href')
    
    (category, area, charge) = getTaobaoRate(rateRankUrl)
    
    rateRankUrl = rateRankUrl[2:len(rateRankUrl)]
    if area:
        area = area.replace("\t", "")
        area = area.replace(" ", "")
    area = area if area != '' else NULL
    charge = charge.replace(",", "") if charge != NULL else NULL
    return (False, userId, shopId, unicode(nickName), shopName, shopUrl, openTime, idTime, rateRankUrl, category, area, charge, companyName, isCompany)
   
def getTaobaoRate(rateRankUrl):
    rateHtml = getHtml("http:" + rateRankUrl)
    category = NULL
    area = NULL
    charge = NULL
    if rateHtml.find("info-block info-block-first") > 0:
        soup = BeautifulSoup(rateHtml, "html.parser")
        lis = soup.find("div", class_="info-block info-block-first").find("ul").find_all("li")
        category = lis[0].find("a").getText().strip()
        area = lis[1].getText().strip().replace("所在地区：", "")
        charge = soup.find("div", class_="charge")
        charge = charge.find("span").getText().strip() if charge else NULL
        charge = charge.replace(",", "") if charge != NULL else NULL
    return (category, area, charge)
   
def getTmallData(soup):
    isCompany = True
    companyName = NULL
    scriptData = getTmallScriptData(soup)
    if scriptData:
        data = getUserId_shopId_userNick(scriptData)
        userId, shopId, nickName = data
        nickName = unquote(str(nickName))
    else:
        return None
    if soup.find("div", class_="slogo") is None:
        return None
    shopData = soup.find("div", class_="slogo").find("a")
    shopName = shopData.getText()
    shopUrl = shopData.get('href')
    shopUrl = shopUrl[2:len(shopUrl)]
    category = NULL
    area = NULL
    charge = NULL
    openTime = NULL
    idTime = NULL
    if soup.find("textarea", class_="ks-datalazyload"):
        infoSoup = soup.find("textarea", class_="ks-datalazyload")
        area = infoSoup.find("li", class_="locus").find("div", class_="right").getText().strip()
        rateRankUrl = infoSoup.find("div", class_="right").find("a").get("href")
        openHtml = infoSoup.find("span", class_="tm-shop-age-content")
        openTime = openHtml.getText() if openHtml else NULL
        rateRankUrl = soup.find("input", id="dsr-ratelink")["value"]
        rateHtml = getHtml("http:" + rateRankUrl)
        soup = BeautifulSoup(rateHtml, "html5lib")
       
    else:
        rateRankUrl = soup.find("input", id="dsr-ratelink")["value"]
        rateHtml = getHtml("http:" + rateRankUrl)
        soup = BeautifulSoup(rateHtml, "html5lib")
        
        if soup.find("textarea", class_="ks-datalazyload"):
            info = soup.find("textarea", class_="ks-datalazyload").getText()
            infoSoup = BeautifulSoup(info, "html.parser")
            area = infoSoup.find("li", class_="locus").find("div", class_="right").getText().strip()
            rateRankUrl = infoSoup.find("div", class_="right").find("a").get("href")
            openHtml = infoSoup.find("span", class_="tm-shop-age-num")
            openTime = openHtml.getText() if openHtml else NULL
    
    if soup.find("div", "left-box"):
        category = soup.find("div", "left-box").find("li").find("a").getText()
        charge = soup.find("div", class_="charge").find("span").getText() if  soup.find("div", class_="charge") else NULL
    
    rateRankUrl = rateRankUrl[2:len(rateRankUrl)]
    if area:
        area = area.replace("\t", "")
        area = area.replace(" ", "")
    area = area if area != '' else NULL
    charge = charge.replace(",", "") if charge != NULL else NULL
    return (True, userId, shopId, unicode(nickName), shopName, shopUrl, openTime, idTime, rateRankUrl, category, area, charge, companyName, isCompany)

def getUserId_shopId_userNick(scriptData):
    if scriptData:
        nickName = scriptData[0].split(":")[1].strip()
        nickName = nickName[1:len(nickName) - 1]
        userId = scriptData[1].split(":")[1].strip()
        userId = userId[1:len(userId) - 1]
        shopId = scriptData[2].split(":")[1].strip()
        shopId = shopId[1:len(shopId) - 1]
        return(userId, shopId, nickName)


def getTmallScriptData(soup):
    for script in soup.find_all('script'):
        script_text = script.get_text()
        if(is_script_g_config(script_text)):
            p_page_config = script_text.strip().split(";")[4]
            data = p_page_config.split("=")[1].strip()
            data = data[1:len(data) - 1]
          
            return data.split(",")
    return None

def getTaobaoScriptData(soup):
    for script in soup.find_all('script'):
        script_text = script.get_text()
        if(is_script_g_config(script_text)):
            p_page_config = script_text.strip().split(";")[2]
            data = p_page_config.split("=")[1].strip()
            data = data[1:len(data)].strip()
            data = data.split(",")
            
            shopId = data[1].split(":")[1].strip()
            shopId = shopId[1:len(shopId) - 1]
            userId = data[3].split(":")[1].strip()
            userId = userId[1:len(userId) - 1]
            nickName = data[4].split(":")[1].strip()
            nickName = nickName[1:len(nickName) - 1]
            return(userId, shopId, unicode(nickName))

    return None

def is_script_g_config(script_text):
        if('window.shop_config' in script_text):
            return True
def getHtml(url, i=0):
    global taobao
    try:
        html = taobao.do_get(url)
        return html
    except RequestException:
        traceback.print_exc()
        print "RequestException:" + url + ":" + str(i)
#         taobao = TaobaoCrawler()
        if i >= 5:
            i = 0
            return None
        time.sleep(30)
        return getHtml(url, i + 1)
    except Exception:
        traceback.print_exc()
        return None


def getShopDetail(url):
    data = findShop(url)  # 淘宝
    if data is not None:
        isTmall, userId, shopId, nickName, shopName, shopUrl, openTime, idTime, rateRankUrl, category, area, charge, companyName, isCompany = data
        province, city = areaGet(area)
        return  (isTmall, userId, shopId, nickName, shopName, shopUrl, openTime, idTime, rateRankUrl, category, province, city, charge, companyName, isCompany)
    
def main(path):
    f = open(path, "r")
    tmall_result = open("./result/tmall_shops", "a")
    taobao_result = open("./result/taobao_shops", "a")
    non = open("./result/notFoundList", "a")
    errors = open("./result/errorList", "a")
    find_list = open("./result/findList", "a")
    log = open("./result/log", "a")
    for line in f:
        line = line.strip()
        line = line.replace("http://", "")
        line = line.replace(".taobao.com", "")
        url = "http://%s.taobao.com" % line.strip()
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\t" + url
        log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\t" + url + "\n")
        try:
            data = findShop(url)
            if data:
                isTmall, userId, shopId, nickName, shopName, shopUrl, openTime, rateRankUrl, category, area, charge, isCompany, companyName = data
                result_line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (userId, shopId, nickName, shopName, shopUrl, openTime, rateRankUrl, category, area, charge, companyName, isCompany) 
                if isTmall:
                    tmall_result.write(result_line + "\n")
                else:
                    taobao_result.write(result_line + "\n")
                find_list.write(url + "\n")
            else:
                non.write(url + "\n")
        except AttributeError:
            traceback.print_exc()
            errors.write(url + "\n")
        except IndexError:
            traceback.print_exc()
            errors.write(url + "\n")
        except RuntimeError:
            traceback.print_exc()
            errors.write(url + "\n")
        except Exception:
            traceback.print_exc()
            errors.write(url + "\n")
    tmall_result.close()
    taobao_result.close()
    non.close()
    errors.close()
    find_list.close()
    log.close()
    f.close() 
        
    
if __name__ == '__main__':
#     path = sys.argv[1]
# # #     path = "./errorList"
#     try:
#         main(path)
#     except Exception:
#         traceback.print_exc()
# #         
    # 10.0.137.25
        url = "https://shop35119070.taobao.com/?spm=a230r.7195193.1997079397.2.CsKHvy"
        data = getShopDetail(url)  # 淘宝
        isTmall, userId, shopId, nickName, shopName, shopUrl, openTime, idTime, rateRankUrl, category, province, city, charge, companyName, isCompany = data
        result_line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (userId, shopId, nickName, shopName, shopUrl, openTime, idTime, rateRankUrl, category, province, city, charge, companyName, isCompany)
        print isTmall, result_line
#         print getShopDetail(url)
#     url= "http://shop100257656.taobao.com"
# #     url = "https://yizhoufs.tmall.com/"
#     url ="http://shop104744602.taobao.com"
#     try:
#         for i in range(100):
#             for item in findShop(url):  #天猫
#                 print item
#     except Exception:
#             traceback.print_exc()
