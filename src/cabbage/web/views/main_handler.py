# -*- encoding: utf-8 -*-
'''
Created on 2016年7月29日

@author: hua
'''
from cabbage.web.api.user_api import UserApi
from cabbage.web.views.base_handler import BaseHandler
import tornado
import traceback
class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("welcome.html")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("new_login.html",title="请登录")
        
    def post(self):
        userName = self.getStrArgument("userName")
        userPwd = self.getStrArgument("userPwd")
        
        if userName is None or userName =="" or userPwd is None or userPwd == "":
            self.render("new_login.html",title="请输入用户名和密码！")
            return
        
        try:
            userApi = UserApi()
            user = userApi.getUser(userName)
            if user is None or user.userPwd != userPwd:
                self.render("new_login.html",title="用户不存在或用户名错误！")
                return
                
            self.session['user'] = user
            self.set_secure_cookie("user", str(userName))
            self.redirect('/', permanent=True)
        except Exception, e:
            traceback.print_exc()
            self.render("new_login.html",title=str(e))