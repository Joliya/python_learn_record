# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals


def lengthOfLongestSubstring1(s):
    """
    无重复最长子串
    :param s:
    :return:
    """

    length = len(s)

    if length < 2:
        return length
    r_len = 0
    for i in range(len(s)):
        sub = []
        sub.append(s[i])
        for j in range(i + 1, length):
            if s[j] in sub:
                l = len(sub)
                if l > r_len:
                    r_len = l
                break
            else:
                sub.append(s[j])
        else:
            l = len(sub)
            if l > r_len:
                r_len = l
    return r_len
