# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.constants import JOB_AUTH_PASS, JOB_RUNNING
from cabbage.data.entity import Job, File, Work
from cabbage.data.zookeeper_store import ZookeeperStore
from cabbage.watch.client_jobs_watch import jobChildWatch, \
    testDataWatch
import logging
import unittest
logging.basicConfig()
class TestWatch(unittest.TestCase):

#     def setUp(self):
#         self.kazooClient = ZookeeperClientHolder.getClient()
#         self.store=ZookeeperStore()
#         self.jobId="job-47778319-7a86-4b2b-a43a-5e2e94504350"
        
    
#     def test_create_job(self):
#             job=Job(jobName="12121212",filePath="1212",
#                      fileType="python",fileName="1212",attachFiles=None,works=None,runStrategy="one")
#             attachFiles=[]
#             attachFiles.append(File(fileName="1212",jobId=job.jobId,jobName=job.jobName,filePath="121212",
#                      fileType="test"))
#             works =[]
#             works.append(Work(ip="1212",port="1212",status="aaa"))
#             job.attachFiles=attachFiles
#             job.works=works
#             self.store.saveJob(job)
            
#     def test_add_watch(self):
# #         self.kazooClient.addDataListener("/cabbage/jobs", testDataWatch)
#         self.kazooClient.addChildListener("/cabbage/jobs", jobChildWatch)
#         
    def test_update_audit_job_pass(self):
        self.kazooClient = ZookeeperClientHolder.getClient()
        self.store=ZookeeperStore()
        self.jobId="job-47778319-7a86-4b2b-a43a-5e2e94504350"
        self.kazooClient.addChildListener("/cabbage/jobs", jobChildWatch)
        self.store.updateAuditStatus(self.jobId,JOB_AUTH_PASS)
        self.store.updateJobStatus(self.jobId,JOB_RUNNING)
     
#     def test_update_job_status(self):
#         self.store.updateJobStatus(self.jobId,JOB_RUNNING)
    
    
if __name__=="__main__":
    unittest.main()