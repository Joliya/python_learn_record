#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   insert_sort.py
@Time    :   2024/12/20 17:04:12
@Author  :   huixuan 
@Desc    :   None

直接插入排序

主要思想
遍历的过程中，将 当前遍历的数和已经遍历过的部分逐一对比，插入到合适的位置
'''


from copy import deepcopy

from leetcode.base_sort.test_unit import test_unit


def insert_sort(nums):
    l = len(nums)
    for i in range(1, l):
        # 先保存一下当前i位置的值，因为后续移位的过程中 i 位置的值可能会发生改变
        temp = nums[i]
        # 已经有序的数组从后往前遍历，目的是把 i 位置的数从后往前移动，直到合适的位置
        for j in reversed(range(i)):
            if temp < nums[j]:
                nums[j + 1], nums[j] = nums[j], nums[j + 1]
            else:
                break
    return nums


def insert_sort2(arr):
    


if __name__ == '__main__':
    print(test_unit([3, 44, 23, 43, 1, 2, 44, 5, 7], insert_sort))
    print(test_unit([23, 11, 7, 29, 33, 59, 8, 20, 9, 3, 2, 6, 10, 44, 83, 28, 5, 1, 0, 36], insert_sort))
