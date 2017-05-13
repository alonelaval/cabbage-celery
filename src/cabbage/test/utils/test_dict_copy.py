# -*- encoding: utf-8 -*-
'''
Created on 2016年11月10日

@author: huawei
'''



aaa = {"111":222,"2222":21212}

bbb = aaa.copy()
print bbb
aaa.clear()
aaa.update({"333":333})

print aaa

print bbb