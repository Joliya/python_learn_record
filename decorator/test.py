# -*- encoding: utf-8 -*-
"""
装饰器使用
"""

from __future__ import absolute_import, unicode_literals

from decorator.hard.compute_time_hard import compute_time_hard_decorator
from decorator.middle.compute_time_middle import compute_time_middle_decorator
from decorator.simple.author_name import author_name_decorator
from decorator.simple.compute_time import compute_func_time_execute_time_decorator


@compute_func_time_execute_time_decorator
def compute_time(x):
    print(f"{x} 计算了时间")


@author_name_decorator(author_name="xiaofang")
def record_author_name(x):
    print(f"{x} 写了这个函数")


@compute_time_middle_decorator(event_name="middle")
def compute_time_middle(event_name="x"):
    print(f"被装饰的函数: {compute_time_middle.__name__}, {event_name}")


@compute_time_hard_decorator
def compute_time_hard(event_name="x"):
    print(f"hard_decorator_event_name: {event_name}")


@compute_time_hard_decorator(event_name="hard_decorator_event_name")
def compute_time_hard_2(event_name="x"):
    print(f"hard_decorator_event_name: {event_name}")


if __name__ == '__main__':
    compute_time("小白")
    record_author_name("小芳")
    print(f"record_author_name 函数增加了作者名称 {record_author_name.author_name}")

    compute_time_middle(event_name="测试middle 计算时间装饰器")
    print("_______________________________")
    compute_time_hard(event_name="hard 测试  装饰器使用的时候 兼容 有无括号1")
    print("_______________________________")
    compute_time_hard_2(event_name="hard 测试  装饰器使用的时候 兼容 有无括号2")

