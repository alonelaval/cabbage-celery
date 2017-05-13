# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''
from cabbage.cabbage_celery.cabbage_holder import CabbageHolder
from cabbage.common.log import logger
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.constants import JOB_AUTH_PASS
from cabbage.data.entity import File, Work, Job
from cabbage.data.zookeeper_store import ZookeeperStore
from cabbage.event.server_jobs_event import JobRunEvent, \
    registerServerEvent
from cabbage.net.server_gevent import GeventStreamServer
from cabbage.watch.server_jobs_watch import jobChildWatch
import threading
import time
import unittest
import zope.event

def start_server():
    geventServer = GeventStreamServer()
    geventServer.start()
    
class TestProcess(unittest.TestCase):
    def setUp(self):
        registerServerEvent()
#     def test_create_job(self):
#         self.kazooClient = ZookeeperClientHolder.getClient()
#         self.store=ZookeeperStore()
#         self.jobId="123456789"
#         job=Job(jobName="12121212",filePath="/Users/hua/workspace/python/cabbage/server_file_path/123456789/test_main.py",jobId=self.jobId,fileType="python",fileName="test_main.py",attachFiles=None,works=None,runStrategy="one")
#         attachFiles=[File(fileName="domains",jobId=job.jobId,jobName=job.jobName,filePath="Users/hua/workspace/python/cabbage/server_file_path/12345678/domains",fileType="text"),
#                          File(fileName="test_task.py",jobId=job.jobId,jobName=job.jobName,filePath="Users/hua/workspace/python/cabbage/server_file_path/123456789/test_task.py",fileType="python")]
#         works =[Work(ip="1212",port="1212",status="aaa")]
#         job.attachFiles=attachFiles
#         job.works=works
#         self.store.saveJob(job)

    def test_update_audit_job_pass(self):
        CabbageHolder.getCabbage()
#         self.kazooClient = ZookeeperClientHolder.getClient()
#         self.store=ZookeeperStore()
#         self.jobId="123456789"
#         self.kazooClient.addChildListener("/cabbage/jobs", jobChildWatch)
#              
# #             
#         t1 = threading.Thread(target=start_server)
#         t1.setDaemon(True)
#         t1.start()
# #         time.sleep(10)
#         self.store.updateAuditStatus(self.jobId,JOB_AUTH_PASS)
#         time.sleep(15)
#         for i in range(10):
        zope.event.notify(JobRunEvent("job-a696407a-20c3-4a07-a68f-260c42157ddb"))
        
#         t1.join()
#         self.store.updateJobStatus(self.jobId,JOB_RUNNING)
        
       
    
    
if __name__=="__main__":
    unittest.main()