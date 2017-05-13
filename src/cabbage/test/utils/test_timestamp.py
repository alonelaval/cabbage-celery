# -*- encoding: utf-8 -*-
'''
Created on 2016年11月7日

@author: huawei
'''

#1788.35323453/(60*60*24)
nTime= 1788.35323453
print nTime/(60*60*24)

print  "day:%s" % (nTime/86400)    
print "hour:%s" % (nTime%86400/3600)    
print "minute:%s" % (nTime%86400%3600/60)