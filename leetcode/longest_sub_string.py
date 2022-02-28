# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals


def lengthOfLongestSubstring(s):
    """
    无重复最长子串
    :param s:
    :return:
    """

    length = len(s)
    ss = []
    for i in range(len(s)):
        sub = []
        sub.append(s[i])
        for j in range(i + 1, length):
            if s[j] in sub:
                ss = sub
                break
            else:
                sub.append(s[j])
    return "".join(ss)
