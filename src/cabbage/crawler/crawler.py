from time import sleep
import json
import os
import requests
import threading



requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'

HEADERS = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "User-Agent":  USER_AGENT}

TIMEOUT = 10

class SessionInLock(requests.Session):

    def __init__(self):
        requests.Session.__init__(self)
#         self.lock = threading.RLock()
    def get(self, url, headers=HEADERS):

#         self.lock.acquire()
        response_ = requests.Session.get(self, url,timeout=TIMEOUT ,headers=headers,verify=False)
#         sleep(0.2)
#         self.lock.release()
        return response_

class Crawler(object):
    
    def do_get(self, url, headers=HEADERS):
        '''
        execute http get method
        '''
#            request = urllib2.Request(url, headers=headers if headers else HEADERS)
            
#            response = urllib2.urlopen(request, timeout=TIMEOUT)
             
        return requests.get(url,headers=headers)
    

class TaobaoCrawler():
    def do_get(self, url, headers=HEADERS):
        SESSION = SessionInLock()   
        SESSION.headers.update({
            'user-agent': USER_AGENT
        })
        
        cookie = os.path.join(os.path.dirname(__file__),"c2.json") 
         
        SESSION.cookies.update(json.load(open(cookie, 'r')))
        return SESSION.get(url).content


if __name__=="__main__":
    print  os.path.join(os.path.dirname(__file__),"c2.json") 




