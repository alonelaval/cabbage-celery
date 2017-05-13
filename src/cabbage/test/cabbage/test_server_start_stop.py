# -*- encoding: utf-8 -*-
'''
Created on 2016年8月1日

@author: hua
'''
from cabbage.server_start import CabbageServer
import threading
import time
import unittest

class TestRun(unittest.TestCase):    
    
    def test_run(self):
        server = CabbageServer()
        def start_server():
            print "-----start-----"
            server.start()
        def stop_server():
            print "------stop----------"
            server.stop()
            
            
        t1 = threading.Thread(target=start_server)
        t1.setDaemon(True)
        t1.start()
        time.sleep(5)
        t2 = threading.Thread(target=stop_server)
        t2.setDaemon(True)
        t2.start()
       
       

if __name__=="__main__":
    unittest.main()