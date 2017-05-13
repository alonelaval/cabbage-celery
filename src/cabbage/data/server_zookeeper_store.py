# -*- encoding: utf-8 -*-
'''
Created on 2016年6月8日

@author: hua
'''
from cabbage.common.log.logger import Logger
from cabbage.common.zookeeper.zookeeper_client_holder import \
    ZookeeperClientHolder
from cabbage.data.store import Store
from cabbage.data.zookeeper_store import ZookeeperStore
from cabbage.utils.util import singleton
from kazoo.retry import KazooRetry
from zope.interface.declarations import implementer
log = Logger.getLogger(__name__)
@singleton
class ServerZookeeperStore(ZookeeperStore):
    def __init__(self):
#         max_tries=1, delay=0.1, backoff=2, max_jitter=0.8,
#                  max_delay=3600, ignore_expire=True, sleep_func=time.sleep,
#                  deadline=None, interrupt=None
#         retry = KazooRetry(max_tries=1000,delay=0.1,backoff=2,max_jitter=0.8,max_delay=3600, ignore_expire=True)
#         self.client= ZookeeperClientHolder.getClient(connection_retry=retry)
        super(type(self),self).__init__(isRetry =True)
