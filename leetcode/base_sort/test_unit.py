"""
测试用例
"""
from copy import deepcopy


def test_unit(nums, func):
    nums_1 = func(deepcopy(nums))
    nums_2 = sorted(deepcopy(nums), key=lambda x: x)
    return nums_1 == nums_2
