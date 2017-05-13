# -*- encoding: utf-8 -*-
'''
Created on 2016年6月7日

@author: hua
'''
import json
import sys
reload(sys)
# sys.setdefaultencoding( "utf-8" )

def list_data():
    area = []
    with open('./location_rules_small.txt','r') as f:
        for line in f.readlines():
            area.append(line)
    return area 

def getPorCity(areas,localtion):
    for area in areas:
        (pro,city)=area.strip().split("\t")
        location = str(localtion)
        if pro in location and city in location:
            return pro,city
        
if __name__=="__main__":
    areas = list_data()
    for line in sys.stdin:
        data = json.loads(line)
        location = data["location"]
        if location:
            (pro,city)= getPorCity(areas,location)
            print pro,city
#             d = location.split(",")
#             if len(d) >1:
#                 pro ,city= getPorCity(areas,d[0],d[1])
#                 print pro ,city
#             else:
#                 d = location.split(" ")
#                 pro ,city= getPorCity(areas,d[0],d[1])
#                 print pro ,city 
                
                
            