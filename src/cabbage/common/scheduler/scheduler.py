#-*- coding: UTF-8 -*- 
'''
Created on 2016年7月21日

@author: huawei
'''
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from cabbage.common.log.logger import Logger
from cabbage.utils.date_util import getNow
from cabbage.utils.util import singleton
log = Logger.getLogger(__name__)
@singleton
class JobManage():
    def __init__(self):
        jobstores = {
            'default': MemoryJobStore()
        }
        executors = {
            'default': ThreadPoolExecutor(50)
#             'processpool': ProcessPoolExecutor(3)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 50
        }
        self.sched = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
        self.addError()
        self.addJobExecuted()
    def addJob(self,func,jobId=None,cron=None,args=[],kwargs={}):
        '''
                                只支持cron的形式
            *　　*　　*　　*　　*　　command
                                分　时　日　月　周　命令
                                
                                第1列表示分钟1～59 每分钟用*或者 */1表示
                                第2列表示小时1～23（0表示0点）
                                第3列表示日期1～31
                                第4列表示月份1～12
                                第5列标识号星期0～6（0表示星期天）
                                第6列要运行的命令
        '''
        if cron is None:
            raise Exception("cron cannot be Null")
        
        (minute,hour,day,month,week)=cron.split(" ")
        self.sched.add_job(func, trigger='cron',id=jobId,hour=hour,minute=minute,day=day,month=month,week=week,args=args,kwargs=kwargs)
        
    def removeJob(self,jobId):
        self.sched.remove_job(jobId)
    
    def start(self):
        self.sched.start()
        
    def shutdown(self):
        self.sched.shutdown()
    
    def printJobs(self):
        self.sched.print_jobs()
        
    def getJobs(self):
        return self.sched.get_jobs()
    
    def addError(self,func=None):
        if func is None:
            func = self.listener
        self.sched.add_listener(func, EVENT_JOB_ERROR)
    
    def addJobExecuted(self,func=None):
        if func is None:
            func = self.listener
        self.sched.add_listener(func, EVENT_JOB_EXECUTED)
        
    def listener(self,event):
        if event.exception:
            log.error("任务【%s】 任务出错 : %s" % (event.job_id,event.traceback))
        else:  
            log.debug( "任务【%s】已经跑完，结束时间 : %s " % (event.job_id,getNow()))


# jobMange = JobManage()