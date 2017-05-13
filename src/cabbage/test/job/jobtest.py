# -*- encoding: utf-8 -*-
'''
Created on 2016年6月1日

@author: hua
'''
# from cabbage.job.IJob import CrawlerJob
import imp


if __name__=='__main__':
#     name="cabbage.test.job.test.Test"
#     name ="cabbage.job.IJob.Test"
    
    a = imp.find_module("test_json", ["/Users/hua/workspace/python/porter/src/com/pingansec/porter/test/"])
    print a
    mod_all = imp.load_module("test_json", a[0], a[1], a[2])
    print mod_all
    aclass = getattr(mod_all, "Test")
    print aclass
    
    
    a = imp.find_module("test_main", ["/Users/hua/workspace/python/cabbage/client_file_path/123456789"])
    print a
    mod_all = imp.load_module("test_main", a[0], a[1], a[2])
    print mod_all
#     aclass = getattr(mod_all, "M")
    print aclass
    
#     files =["/Users/hua/workspace/python/porter/src/com/pingansec/porter/test/test_json.py"]
#     attch=[open("/Users/hua/workspace/python/cabbage/src/com/pingansec/cabbage/test/job/domains")]
#     crawler = CrawlerJob(name,files,attch)
#     crawler.start()