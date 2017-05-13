# -*- encoding: utf-8 -*-
'''
Created on 2016年11月2日

@author: huawei
'''
from cabbage.data.store_factory import storeFactory
import traceback
def excute(callback,*args, **kwargs):
        def _excute(cls,*args, **kwargs):
            store =  storeFactory.getStore()
            try:
                return callback(cls,store,*args, **kwargs)
            except Exception as e:
                traceback.print_exc()
                raise e
            finally:
                storeFactory.returnStroe(store)
                
        return _excute