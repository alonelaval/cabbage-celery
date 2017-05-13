# -*- encoding: utf-8 -*-
'''
Created on 2016年7月29日

@author: hua
'''
from cabbage.web.views.base_handler import BaseHandler
class MainHandler(BaseHandler):
    def get(self):
        self.render("welcome.html")

class LoginHandler(BashHandler):