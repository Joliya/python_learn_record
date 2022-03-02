# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals


from typing import List

key = 'codehole'

import redis

client = redis.StrictRedis(host='192.168.21.63', port=6379)
# for i in range(1000):
#     client.pfadd(key, "user%d" % i)
#     total = client.pfcount(key)
#     if total != i+1:
#         print(total, i+1)
#         break

# client.set("zhangsna", 19)
client.delete(key)
for i in range(100000):
    client.execute_command('set', key, 'user%d' % i)
    ret = client.execute_command('get', key, 'user%d' % i)
    if ret == 0:
        print(i)
        break


# import time
#
# class Funnel(object):
#
#     def __init__(self, capacity, leaking_rate):
#         self.capacity = capacity  # 漏斗容量
#         self.leaking_rate = leaking_rate  # 漏嘴流水速率
#         self.left_quota = capacity  # 漏斗剩余空间
#         self.leaking_ts = time.time()  # 上一次漏水时间
#
#     def make_space(self):
#         now_ts = time.time()
#         delta_ts = now_ts - self.leaking_ts  # 距离上一次漏水过去了多久
#         delta_quota = delta_ts * self.leaking_rate  # 又可以腾出不少空间了
#         if delta_quota < 1:  # 腾的空间太少，那就等下次吧
#             return
#         self.left_quota += delta_quota  # 增加剩余空间
#         self.leaking_ts = now_ts  # 记录漏水时间
#         if self.left_quota > self.capacity:  # 剩余空间不得高于容量
#             self.left_quota = self.capacity
#
#     def watering(self, quota):
#         self.make_space()
#         if self.left_quota >= quota:  # 判断剩余空间是否足够
#             self.left_quota -= quota
#             return True
#         return False
#
#
# funnels = {}  # 所有的漏斗
#
# # capacity  漏斗容量
# # leaking_rate 漏嘴流水速率 quota/s
# def is_action_allowed(
#         user_id, action_key, capacity, leaking_rate):
#     key = '%s:%s' % (user_id, action_key)
#     funnel = funnels.get(key)
#     if not funnel:
#         funnel = Funnel(capacity, leaking_rate)
#         funnels[key] = funnel
#     return funnel.watering(1)
#
#
# for i in range(20):
#     print(is_action_allowed('laoqian', 'reply', 15, 0.5))
