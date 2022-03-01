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


def lengthOfLongestSubstring2(s):
    """
    无重复最长子串( 滑动窗口 解题思路)
    :param s: p w w k e w
    :return:
    """
    # 当前不重复集合
    lookup = set()
    cur_len = 0
    max_len = 0
    # 指针移动的位置
    left = 0

    # 循环 字符串长度次数， O(n) 时间复杂度
    for i in range(len(s)):
        cur_len += 1  # 每次循环指针后移，此时 当前 不重复长度 + 1
        while s[i] in lookup:
            # 如果 元素 在 集合中，则已经重复， 则从当前位置的最左边开始 移除元素， 直到 移除 当前 i 位置元素相同的元素
            lookup.remove(s[left])
            left += 1  # 滑动窗口左边左边始终是 不重复元素的 第一个元素的位置
            cur_len -= 1  # 每次移除元素 当前 不重复元素长度 就减 1

        max_len = cur_len if cur_len > max_len else max_len
        lookup.add(s[i])
    return max_len


def lengthOfLongestSubstring(self, s: str) -> int:
    if not s:return 0
    left = 0
    lookup = set()
    n = len(s)
    max_len = 0
    cur_len = 0
    for i in range(n):
        cur_len += 1
        while s[i] in lookup:
            lookup.remove(s[left])
            left += 1
            cur_len -= 1
        if cur_len > max_len:max_len = cur_len
        lookup.add(s[i])
    return max_len
