# -*- encoding: utf-8 -*-
'''
Created on 2016年6月6日

@author: hua
'''
from cabbage.common.serialize.json_serialization import \
    JosnSerialization
from cabbage.common.serialize.pickle_serialization import \
    PickleSerialization


SERIALEZE_HOLDER={
            JosnSerialization.TYPE:JosnSerialization,
            PickleSerialization.TYPE:PickleSerialization
            }