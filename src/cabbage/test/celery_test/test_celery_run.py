# -*- encoding: utf-8 -*-
'''
Created on 2016年9月23日

@author: huawei
'''
from cabbage.test.celery_test.test_celery import T
import time

    
class Test():
    def run(self):
        results =[]
        for i in range(10):
            result2 = T.run2.apply_async(args=(4, 5))
            print "result2:"+str(result2)
            results.append(result2)
        time.sleep(10)     
        for result in results:
            print result.status
            print "result:"+str(result.result)
#             if result2.ready():
#                 print result2.status
#                 print "result2:"+str(result2.result)
            
def test():
    t = Test()
    t.run()
#     t =T(1,2)
#     t.run()
    
test()