"""
冒泡排序算法
"""
from leetcode.base_sort.test_unit import test_unit


def bubble_sort(nums):
    """
    冒泡排序
    :param nums:
    :return:
    """
    l = len(nums)
    for i in range(l):
        for j in range(i + 1, l):
            if nums[i] > nums[j]:
                nums[i], nums[j] = nums[j], nums[i]
    return nums


if __name__ == '__main__':
    print(test_unit([23, 11, 7, 29, 33, 59, 8, 20, 9, 3, 2, 6, 10, 44, 83, 28, 5, 1, 0, 36], bubble_sort))
