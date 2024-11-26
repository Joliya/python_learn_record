# -*- encoding: utf-8 -*-
"""
两数之和
"""

from __future__ import absolute_import, unicode_literals
from typing import List


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


class Solution2:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d_to_idx = {}
        for idx, i in enumerate(nums):
            d = target - i
            if d in d_to_idx:
                return [d_to_idx[d], idx]
            d_to_idx[i] = idx
        return [0, 0]


if __name__ == '__main__':
    nums = [2,7,11,15]
    target = 9
    Solution2().twoSum(nums=nums, target=target)
