# -*- encoding: utf-8 -*-
"""
通用数据结构
"""

from __future__ import absolute_import, unicode_literals


class Node:

    def __init__(self, value, node):
        self.value = value
        self.next = node

    def __str__(self):
        return f"value: {self.value}"
