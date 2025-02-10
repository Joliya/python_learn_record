"""
@File    :   selection_sort.py
@Time    :   2024/12/20 11:40:54
@Author  :   huixuan 
@Desc    :   选择排序


首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置。

再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。

重复第二步，直到所有元素均排序完毕。
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


def selection_sort(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[i]:
                arr[i], arr[j] = arr[j], arr[i]
    return arr


if __name__ == '__main__':
    print(test_unit([23, 11, 7, 29, 33, 59, 8, 20, 9, 3, 2, 6, 10, 44, 83, 28, 5, 1, 0, 36], simple_select_sort))
