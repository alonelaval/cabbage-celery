# -*- encoding: utf-8 -*-
'''
Created on 2016年7月29日

@author: hua
'''

import base64
import os
import uuid



def gen_cookie_secret():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

# print os.path.dirname(__file__)
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret=gen_cookie_secret(),
    static_url_prefix='/static/',
    login_url='/login',
    
)



