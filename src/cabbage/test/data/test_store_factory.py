# -*- encoding: utf-8 -*-
'''
Created on 2016年11月2日

@author: huawei
'''
# -*- encoding: utf-8 -*-
from cabbage.common.pool.connection_pool import ObjectPoolTimeout, \
    ConnectionObjectPool
from cabbage.data.store_factory import StoreFactory
from cabbage.data.store_holder import StoreHolder
from time import sleep, time
import threading
import unittest
'''
Created on 2016年10月31日

@author: huawei
'''


class TestOjbectPool(unittest.TestCase):

    def setUp(self):
        self.num_created = 0

#     def _create(self):
#         self.num_created += 1
#         return StoreHolder.getStore()

    def _run_threads(self, target, num_threads):
        threads = [threading.Thread(target=target) for i in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def test_create(self):
        print "test_create-----begin"
        pool = StoreFactory()
        self._run_threads(pool.getStore, 100)
#         self.assertEqual(pool._size, 100)
#         self.assertEqual(self.num_created, 100)
        print "test_create-----end"

    def test_max_size(self):
        print "test_max_size-----begin"
        pool =StoreFactory(max_size=10)# ConnectionObjectPool(self._create, max_size=10)
        def get_and_put():
            item = pool.getStore()
#             print item
            sleep(0.01)
            pool.returnStroe(item)
        self._run_threads(get_and_put, 100)
#         self.assertGreater(pool._size, 0)
#         self.assertLessEqual(pool._size, 10)
#         self.assertGreater(self.num_created, 0)
        print "test_max_size-----end"

    def test_blocking(self):
        print "test_blocking-----begin"
        pool =StoreFactory(max_size=1)# ConnectionObjectPool(self._create, max_size=1)
        item = pool.getStore()
        elapsed = []
        def get():
            begin = time()
            pool.getStore()
            elapsed.append(time() - begin)
        t = threading.Thread(target=get)
        t.start()
        sleep(0.01)
        pool.returnStroe(item)
        t.join()
        self.assertGreater(elapsed[0], 0.01)
        print "test_blocking-----end"

    def test_timeout(self):
        print "test_timeout-----begin"
        pool =StoreFactory(max_size=1)# ConnectionObjectPool(self._create, max_size=1)
        item = pool.getStore()
        self.assertRaises(ObjectPoolTimeout, pool.getStore, timeout=0.01)
        pool.returnStroe(item)
        pool.getStore(timeout=0.0) # shouldn't raise
        print "test_timeout-----end"

    def test_with(self):
        print "test_with-----begin"
        pool = StoreFactory(max_size=1)#ConnectionObjectPool(self._create, max_size=1)
#         self.assertEqual(pool._size, 0)
        with pool.store():
            pass
#         self.assertEqual(self.num_created, 1)
#         self.assertEqual(len(pool._items), 1)
#         self.assertEqual(pool._size, 1)
        try:
            with pool.store():
                raise RuntimeError
        except RuntimeError:
            print "excee"
            pass
        print "test_with-----end"
#         self.assertEqual(self.num_created, 1)
#         self.assertEqual(len(pool._items), 1)
#         self.assertEqual(pool._size, 1)
        
#     def test_timeout2(self):
#         pool = StoreFactory(max_size=1)
#         item = pool.getStore()
#         self.assertRaises(ObjectPoolTimeout, pool.get, timeout=0.01)
#         pool.returnStroe(item)
#         pool.getStore(timeout=0.0) # shouldn't raise

if __name__ == '__main__':
    unittest.main()