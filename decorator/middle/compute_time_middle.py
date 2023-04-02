# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

from functools import wraps


def compute_time_middle_decorator(event_name=""):
    """
    使用的时候只能带括号
    :return:
    """
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            print("前置任务")
            print(f"event_name: {event_name}")
            print(args, kwargs)
            func(*args, **kwargs)
            print("后置任务")
        return inner

    return outer



