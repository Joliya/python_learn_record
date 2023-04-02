# -*- encoding: utf-8 -*-
"""
统计函数的执行时间
"""

from __future__ import absolute_import, unicode_literals

import time


def compute_func_time_execute_time_decorator(func):
    """
    输出函数的执行时间
    :return:
    """
    def execute(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        print((time.time() - t1))
    return execute
