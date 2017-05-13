# -*- encoding: utf-8 -*-
'''
Created on 2016年8月1日

@author: hua
'''
from torndsession.sessionhandler import SessionBaseHandler
class BaseHandler(SessionBaseHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")
    def getCurrentUserFromSession(self):
        return self.session['user'] 
    def getArgument(self,name):
        return self.getStrArgument(name)
    
    def getArguments(self,name):
        return self.get_arguments("%s[]"%name)
    
    def getStrArgument(self,name):
        param =self.get_argument(name,default=None)
        if param:
            return str(param)
        else:
            None
    
    def getCurrentUserFromSession(self):
        if 'user' in self.session:
            return self.session['user'] 
        else:
#             user = User().getUser(self.get_current_user())
            self.session['user'] = user
            return user
