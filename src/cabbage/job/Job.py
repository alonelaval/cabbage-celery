# -*- encoding: utf-8 -*-
'''
Created on 2016年6月1日

@author: hua
'''
from zope.interface.declarations import implementer
from zope.interface.interface import Interface

class IJob(Interface):
    '''
        job
    '''
    def name(self):
        pass
    def start(self):
        pass
    def stop(self):
        pass
    def restart(self):
        pass
    def pause(self):
        pass
    def forward(self):
        pass
    def run(self,*args, **kwargs):
        pass
    
    
@implementer(IJob)
class AbstractJob(object):
    def __init__(self,job):
        self.job=job

class AbstractFileJob(AbstractJob):
    def __init__(self,job):
        self.job
        
    
class ShellScriptJob(AbstractFileJob):
    pass
    
# class CrawlerJob(PythonScriptJob):
#     def __init__(self,job):
#         self.job
#         super(CrawlerJob,self).__init__(self.name,self.files)
#     def start(self):
#         for f in self.files:
#             try:
#                 execfile(f)
#             except Exception:
#                 traceback.print_exc()
#                 raise  Exception
#         self.obj=instantiate(self.name)
#         print self.obj
#     def run(self,*args, **kwargs):
#         self.obj.run(*args,**kwargs)
        
if __name__=='__main__':
#     print IJob.implementedBy(CrawlerJob)
    pass
    
    

    
    
    
    