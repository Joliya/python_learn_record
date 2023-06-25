"""
简单选择排序

每次选取未排序的最大值，与未排序的最后一个数据交换
"""
from leetcode.base_sort.test_unit import test_unit


def simple_select_sort(nums):
    """
    简单选择排序
    :param nums:
    :return:
    """
    l = len(nums)
    for i in range(l):
        max_index = 0
        for j in range(l - i):
            if nums[j] > nums[max_index]:
                max_index = j
        nums[max_index], nums[l - 1 - i] = nums[l - 1 - i], nums[max_index]
    return nums


if __name__ == '__main__':
    print(test_unit([23, 11, 7, 29, 33, 59, 8, 20, 9, 3, 2, 6, 10, 44, 83, 28, 5, 1, 0, 36], simple_select_sort))
