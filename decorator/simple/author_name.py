# -*- encoding: utf-8 -*-
"""
作者名称装饰器
"""

from __future__ import absolute_import, unicode_literals


def author_name_decorator(author_name=""):
    """记录作者名称"""
    def call(func):
        print(author_name)
        func.author_name = author_name
        return func
    return call
