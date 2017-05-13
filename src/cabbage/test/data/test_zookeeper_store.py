# -*- encoding: utf-8 -*-
'''
Created on 2016年6月12日

@author: hua
'''
from cabbage.data.entity import Job, File, Work, Auth, User
from cabbage.data.store_holder import StoreHolder
from cabbage.utils.host_name import getHostName
from unittest.case import TestCase
import unittest.main

class TestZookeeperStore(TestCase):
    def setUp(self):
        self.store=StoreHolder.getStore()
        
    def save_job(self):
        
        job=Job(jobName="12121212",filePath="1212",auditStatus="a1212",
                 fileType="python",fileName="1212",status="1212",attachFiles=None,works=None,runStrategy="one")
        attachFiles=[]
        attachFiles.append(File(fileName="1212",jobId=job.jobId,jobName=job.jobName,filePath="121212",
                 fileType="test"))
        works =[]
        works.append(Work(ip="1212",port="1212",status="aaa"))
        job.attachFiles=attachFiles
        job.works=works
        self.store.saveJob(job)
   
#     def test_get_jobs(self):
#         jobs = self.store.getJobs()
#         for job in jobs:
#             print job.jobName
    def test_get_job(self):
        jobId=u"job-264f2056-59c1-42ed-808d-d1be0879d7cb"
        print self.store.getJob(jobId)
            
    def save_file(self):
        jobId="job-9acc18b2-9bb2-4fbf-9c2b-95b77fe7bdd6"
        jobName="12121212"
        f = File(fileName="11212",jobId=jobId,jobName=jobName,filePath="121212",
                 fileType="python")
        self.store.saveFile(f)
    
#     def test_get_files(self):
#         files = self.store.getFiles()
#         for f in files:
#             print f.jobId
#     
    def save_auth(self):
        jobId="job-9acc18b2-9bb2-4fbf-9c2b-95b77fe7bdd6"
        auth = Auth(jobId=jobId,auditUser="huawei",auditStauts="False")
        self.store.saveAuth(auth)
        
#     def test_get_auths(self):
#         auths = self.store.getAuths()
#         for auth in auths:
#             print "jobID"+auth.jobId
#             print "auditTime:"+str(auth.auditTime)
            
    def save_user(self):
        user = User(userName="huawei",userPwd="121212",isAdmin="False")
        self.store.saveUser(user)
        
#     def test_get_users(self):
#         users = self.store.getUsers()
#         for user in users:
#             print user.userName
#             print type(user.isAdmin)
    
    def save_work(self):
        work =Work(ip="192.168.108.211",port="1024",status="status")
        self.store.saveWork(work)
        
#     def test_get_work(self):
#         hostName=getHostName()
#         work = self.store.getWork(hostName)
#         self.assertEqual(hostName, work.hostName, "lll")
#         self.assertEqual("192.168.108.211", work.ip, "lll")
#         self.assertEqual("1024", work.port, "lll")
        
        
if __name__=='__main__':
    
    unittest.main()
    
    
    
    