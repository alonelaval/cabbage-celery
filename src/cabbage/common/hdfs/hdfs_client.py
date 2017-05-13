# -*- encoding: utf-8 -*-
'''
Created on 2016年9月21日

@author: huawei
'''
from cabbage.constants import TYPE, FILE, DIRECTORY, FILE_SIZE
from hdfs.client import Client

class HdfsClient(object):
    def __init__(self,url=None):
        self.url=url
        self.client = Client(url=url)
        
    def ls(self,path):
        return self.client.list(path)
    
    def isFile(self,path):
        result=  self.client.status(path, strict=False)
        if result:
                return result[TYPE] ==FILE
        else:
            return False
    def mkdir(self,path):
        self.client.makedirs(path, permission=777)  
        
    def isDirectory(self,path):
        result=  self.client.status(path, strict=False)
        if result:
                return result[TYPE] == DIRECTORY
        else:
            return False
    def upload(self,localSourcePath,remoteDistPath):
        self.client.upload(remoteDistPath, localSourcePath,overwrite=True)
    def dowload(self,remoteSourcePath,localDistPath):
        self.client.download(remoteSourcePath,localDistPath,overwrite=True)
        
    def put(self,localSourcePath,remoteDistPath):
        with open(localSourcePath,"r") as reader,self.client.write(remoteDistPath) as writer:
            data =reader.read(FILE_SIZE)
            while data  != "" :
                writer.write(data)
                data =reader.read(FILE_SIZE)
                
    def get(self,remoteSourcePath,localDistPath):
        with self.client.read(remoteSourcePath,chunk_size=FILE_SIZE) as reader,open(localDistPath,"a+") as writer:
            for chunk in reader:
                writer.write(chunk)
        
    