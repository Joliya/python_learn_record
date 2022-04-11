# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

from functools import wraps


def compute_time_hard_decorator(f=None, event_name=""):
    """
    调用此装饰器的时候可 戴 括号， 也可不带括号
    :param f:
    :return:
    """

    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            print(f"hard 装饰器: {event_name}")
            print(args, kwargs)

            return func(*args, **kwargs)
        return inner

    if not f:
        print(f"没走 参数 函数： {f}")
        return outer
    print(f"走了 参数 函数： {f}")
    return outer(f)
