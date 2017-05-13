# -*- encoding: utf-8 -*-
'''
Created on 2016年9月20日

@author: huawei
'''
from cabbage.data.store_holder import StoreHolder
import unittest


tasks={u'test_both_task.TestBothTask': {'taskFailed': 0, 'taskRuntime': 0.02014401900305529, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.01990509033203125}, 
        u'test_ubuntu_task.TestUbuntuTask': {'taskFailed': 0, 'taskRuntime': 0.026165831000980688, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.028292179107666016},
         u'test_mac_task.TestMacTask': {'taskFailed': 0, 'taskRuntime': 0.011778828997194069, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.010283231735229492}, 
         u'test_fail_task.TestFailTask': {'taskFailed': 4, 'taskRuntime': 0.007163269998272881, 'taskSucceeded': 6, 'taskCount': 10, 'taskQueueTime': 0.00635528564453125}}


works= {u'huamac': {'taskRuntime': 0.026697580997279147, 'taskSucceeded': 21, 'taskCount': 25, 'taskFailed': 4}, 
        u'ubuntu': {'taskRuntime': 0.03855436800222378, 'taskSucceeded': 15, 'taskCount': 15}}

workTasks= {u'huamac': {u'test_both_task.TestBothTask': {'taskRuntime': 0.007755482001812197, 'taskSucceeded': 5, 'taskCount': 5, 'taskQueueTime': 0.005683183670043945}, 
                        u'test_mac_task.TestMacTask': {'taskRuntime': 0.011778828997194069, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.010283231735229492}, 
                        u'test_fail_task.TestFailTask': {'taskRuntime': 0.007163269998272881, 'taskSucceeded': 6, 'taskFailed': 4, 'taskQueueTime': 0.00635528564453125,'taskCount': 10}},
         u'ubuntu': {u'test_both_task.TestBothTask': {'taskRuntime': 0.012388537001243094, 'taskSucceeded': 5, 'taskCount': 5, 'taskQueueTime': 0.014221906661987305}, 
                     u'test_ubuntu_task.TestUbuntuTask': {'taskRuntime': 0.026165831000980688, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.028292179107666016}}} 


taskFail= {u'test_fail_task.TestFailTask': {u'huamac': 4}}
taskReceived= {u'test_both_task.TestBothTask': {u'huamac': 5, u'ubuntu': 5}, u'test_mac_task.TestMacTask': {u'huamac': 10}, u'test_fail_task.TestFailTask': {u'huamac': 10}, u'test_ubuntu_task.TestUbuntuTask': {u'ubuntu': 10}}
taskSent= {u'test_both_task.TestBothTask': 10, u'test_mac_task.TestMacTask': 10, u'test_fail_task.TestFailTask': 10, u'test_ubuntu_task.TestUbuntuTask': 10}
taskSucceeded= {u'test_fail_task.TestFailTask': {u'huamac': {'taskRuntime': 0.007163269998272881, 'taskCount': 6, 'taskQueueTime': 0.00635528564453125}}, u'test_both_task.TestBothTask': {u'huamac': {'taskRuntime': 0.007755482001812197, 'taskCount': 5, 'taskQueueTime': 0.005683183670043945}, u'ubuntu': {'taskRuntime': 0.012388537001243094, 'taskCount': 5, 'taskQueueTime': 0.014221906661987305}}, u'test_mac_task.TestMacTask': {u'huamac': {'taskRuntime': 0.011778828997194069, 'taskCount': 10, 'taskQueueTime': 0.010283231735229492}}, u'test_ubuntu_task.TestUbuntuTask': {u'ubuntu': {'taskRuntime': 0.026165831000980688, 'taskCount': 10, 'taskQueueTime': 0.028292179107666016}}}




tasks= {u'test_both_task.TestBothTask': {'taskFailed': 0, 'taskRuntime': 0.024148837004759116, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.024232149124145508}, u'test_mac_task.TestMacTask': {'taskFailed': 0, 'taskRuntime': 0.010965680001390865, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.00859522819519043}, u'test_fail_task.TestFailTask': {'taskFailed': 6, 'taskRuntime': 0.004448175001016352, 'taskSucceeded': 4, 'taskCount': 10, 'taskQueueTime': 0.0037589073181152344}, u'test_ubuntu_task.TestUbuntuTask': {'taskFailed': 0, 'taskRuntime': 0.020092877002753085, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.022061824798583984}}
works= {u'huamac': {'taskRuntime': 0.02168561500729993, 'taskSucceeded': 19, 'taskCount': 25, 'taskFailed': 6}, u'ubuntu': {'taskRuntime': 0.03796995400261949, 'taskSucceeded': 15, 'taskCount': 15}}
workTasks= {u'huamac': {u'test_both_task.TestBothTask': {'taskRuntime': 0.0062717600048927125, 'taskSucceeded': 5, 'taskCount': 5, 'taskQueueTime': 0.006188869476318359}, u'test_fail_task.TestFailTask': {'taskRuntime': 0.004448175001016352, 'taskSucceeded': 4, 'taskFailed': 6, 'taskQueueTime': 0.0037589073181152344, 'taskCount': 10}, u'test_mac_task.TestMacTask': {'taskRuntime': 0.010965680001390865, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.00859522819519043}}, u'ubuntu': {u'test_both_task.TestBothTask': {'taskRuntime': 0.017877076999866404, 'taskSucceeded': 5, 'taskCount': 5, 'taskQueueTime': 0.01804327964782715}, u'test_ubuntu_task.TestUbuntuTask': {'taskRuntime': 0.020092877002753085, 'taskSucceeded': 10, 'taskCount': 10, 'taskQueueTime': 0.022061824798583984}}} 
taskFail= {u'test_fail_task.TestFailTask': {u'huamac': 6}}

taskReceived= {u'test_both_task.TestBothTask': {u'huamac': 5, u'ubuntu': 5}, u'test_ubuntu_task.TestUbuntuTask': {u'ubuntu': 10}, u'test_fail_task.TestFailTask': {u'huamac': 10}, u'test_mac_task.TestMacTask': {u'huamac': 10}}
taskSent= {u'test_both_task.TestBothTask': 10, u'test_ubuntu_task.TestUbuntuTask': 10, u'test_fail_task.TestFailTask': 10, u'test_mac_task.TestMacTask': 10}
taskSucceeded= {u'test_both_task.TestBothTask': {u'huamac': {'taskRuntime': 0.0062717600048927125, 'taskCount': 5, 'taskQueueTime': 0.006188869476318359}, u'ubuntu': {'taskRuntime': 0.017877076999866404, 'taskCount': 5, 'taskQueueTime': 0.01804327964782715}}, u'test_ubuntu_task.TestUbuntuTask': {u'ubuntu': {'taskRuntime': 0.020092877002753085, 'taskCount': 10, 'taskQueueTime': 0.022061824798583984}}, u'test_fail_task.TestFailTask': {u'huamac': {'taskRuntime': 0.004448175001016352, 'taskCount': 4, 'taskQueueTime': 0.0037589073181152344}}, u'test_mac_task.TestMacTask': {u'huamac': {'taskRuntime': 0.010965680001390865, 'taskCount': 10, 'taskQueueTime': 0.00859522819519043}}}


class TestRun(unittest.TestCase):    
    
    def test_run(self):
        print workTasks 
        print id(workTasks)
        copy=workTasks.copy()
        workTasks.clear()
        print workTasks
        print copy
        print id(copy)
        
        
    

if __name__=="__main__":
    unittest.main()