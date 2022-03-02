# -*- encoding: utf-8 -*-
"""
数字是否对称
"""

from __future__ import absolute_import, unicode_literals


class Solution:
    def reverse(self, x: int) -> int:
        y = [1, -1][x < 0] * int(str(abs(x))[::-1])
        return y if y.bit_length() < 32 else 0
