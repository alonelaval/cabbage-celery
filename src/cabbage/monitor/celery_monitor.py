# -*- encoding: utf-8 -*-
'''
Created on 2016年6月15日

@author: hua
'''
# from cabbage.common.scheduler.scheduler_holder import \
#     JobManageHolder
from cabbage.constants import TASK_FAILED, TASK_SUCCEEDED, \
    TASK_SENT, TASK_STARTED, WORKER_ONLINE, WORKER_OFFLINE, TASK_RECEIVED, \
    TASK_REVOKED, TASK_RETRIED
# from cabbage.monitor.monitor_stat_action import monitorJob
# from cabbage.monitor.monitor_handlers import registerMoniters
from cabbage.monitor.monitor_manager import monitorManager

# registerMoniters()
# JobManageHolder.getJobManage().addJob(monitorJob,jobId="monitor",cron="*/1 * * * *")

def cabbage_monitor(app):
    state = app.events.State()
    def task_failed(event):
#         print state.alive_workers()
        state.event(event)
        monitorManager.fire(TASK_FAILED,state,event,app)
        
    def task_succeeded(event):
        state.event(event)
        monitorManager.fire(TASK_SUCCEEDED,state,event,app)
        
    def task_sent(event):
        state.event(event)
        monitorManager.fire(TASK_SENT,state,event,app)
        
    def task_received(event):
        state.event(event)
        monitorManager.fire(TASK_RECEIVED,state,event,app)
    def worker_online(event):
        state.event(event)
        monitorManager.fire(WORKER_ONLINE,state,event,app)
    def worker_offline(event):
        state.event(event)
#         print state,event
        monitorManager.fire(WORKER_OFFLINE,state,event,app)
        
    def task_started(event):
        state.event(event)
        monitorManager.fire(TASK_STARTED,state,event,app)
        
    def task_revoked(event):
        state.event(event)
        monitorManager.fire(TASK_REVOKED,state,event,app)
        
    def task_retried(event):
        state.event(event)
        monitorManager.fire(TASK_RETRIED,state,event,app)
        
    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed':task_failed,
                'task-sent':task_sent,
                'task-received':task_received,
                'task-started':task_started,
                'task-succeeded':task_succeeded,
                'task-revoked':task_revoked,
                'task-retried':task_retried,
                'worker-online': worker_online,
                'worker-offline': worker_offline
        })
        recv.capture(limit=None, timeout=None, wakeup=True)
               
