# -*- encoding: utf-8 -*-
"""
两数之和
"""

from __future__ import absolute_import, unicode_literals


class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for idx, i in enumerate(nums):
            sup = target - i
            print('i=%s' % i)
            print('sup=%s' % sup)
            if not nums.__contains__(sup):
                continue
            index = nums.index(sup)
            print('index=%s' % index)
            if index == idx:
                continue
            return [idx, index]
