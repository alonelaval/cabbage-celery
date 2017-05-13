# coding=utf-8
'''
Created on 2012-9-21

@author: Administrator
'''
domain_stuffix = (".gov.mo",
        ".com.tw",
        ".com.mo",
        ".co.cc",
        ".ce.ms",
        ".osa.pl",
        ".c.la",
        ".com.hk",
        ".net.in",
        ".edu.tw",
        ".org.tw",
        ".bij.pl",
    
        ".ac.cn",
        ".ah.cn",
        ".bj.cn",
        ".com.cn",
        ".cq.cn",
        ".fj.cn",
        ".gd.cn",
        ".gov.cn",
        ".gs.cn",
        ".gx.cn",
        ".gz.cn",
        ".ha.cn",
        ".hb.cn",
        ".he.cn",
        ".hi.cn",
        ".hk.cn",
        ".hl.cn",
        ".hn.cn",
        ".jl.cn",
        ".js.cn",
        ".jx.cn",
        ".ln.cn",
        ".mo.cn",
        ".net.cn",
        ".nm.cn",
        ".nx.cn",
        ".org.cn",
        ".qh.cn",
        ".sc.cn",
        ".sd.cn",
        ".sh.cn",
        ".sn.cn",
        ".sx.cn",
        ".tj.cn",
        ".tw.cn",
        ".xj.cn",
        ".xz.cn",
        ".yn.cn",
        ".zj.cn",
        
        ".nl.ae",
        ".org.uk",
        ".org.nz",
        ".org.bz",
        ".org.au",
        ".com.nu",
        ".com.my",
        ".com.au",
        ".co.uk",
        ".co.kr",
        ".co.jp",
        ".nu.ae",
        ".nl.ae",
        ".com.au",
        ".cf.gs",

        ".com.cn",
        ".net.cn",
        ".org.cn",
        ".edu.cn",
        
        ".com",
        ".cn",
        ".mobi",
        ".tel",
        ".asia",
        ".net",
        ".org",
        ".name",
        ".me",
        ".info",
        ".cc",
        ".hk",
        ".biz",
        ".tv",
        
        ".la",
        ".fm",
        ".cm",
        ".am",

        ".sh",
        
        ".us",
        ".in",
        ".ro",
        ".ru",
        ".hu",
        ".tk",
        ".co",
        ".cx",
        ".at",
        ".tw",
        ".ws",
        ".vg",
        ".vc",
        ".uz",
        ".to",
        ".tl",
        ".th",
        ".tf",
        ".tc",
        ".st",
        ".so",
        ".sk",
        ".sg",
        ".sc",
        ".pl",
        ".pe",
        ".nu",
        ".nf",
        ".ne",
        ".my",
        ".mu",
        ".ms",
        ".mo",
        ".lv",
        ".lt",
        ".lc",
        ".jp",
        ".it",
        ".io",
        ".im",
        ".ie",
        ".gs",
        ".gp",
        ".gl",
        ".gg",
        ".gd",
        ".fr",
        ".fi",
        ".eu",
        ".edu",
        ".dk",
        ".de",
        ".cz",
        ".ch",
        ".ca",
        ".bi",
        ".be",
        ".au",
        ".ae",
        ".wang",)
def exec_domain(url):
    if(url is None or url == ''):
        return url
    url = url.replace(" ", "")
    url = url.replace("https://", "")
    url = url.replace("http://", "")
    colonIndex = url.find(":")
    if(colonIndex>0):
        url = url[0:colonIndex]
    ganIndex = url.find("/")
    if(ganIndex>0):
        url = url[0:ganIndex]
    arr = url.split(".")
    domain = ""
    star = 0
    if(arr[0]=="www"):
        star = 1
    for i in range(star,len(arr)):
        domain = domain +  arr[i]
        if(i!=len(arr)-1):
            domain += "."
    return domain
def exec_primarydomain(url):
    if(url is None or url == ''):
        return url
    domain = exec_domain(url)
    for  str in domain_stuffix:
        if(domain.endswith(str)):
            pos = len(domain)-len(str)
            filterPostfix = domain[0:pos]
            arr = filterPostfix.split(".")
            firstDomain = arr[len(arr)-1]+str
            if(domain.endswith(firstDomain)):
                return firstDomain
    return domain