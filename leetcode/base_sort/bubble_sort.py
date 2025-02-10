"""
@File    :   bubble_sort.py
@Time    :   2024/12/20 11:16:05
@Author  :   huixuan 
@Desc    :   冒泡排序

依次比较相邻元素，较大的后移，每次循环都会将最大的放后面

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


def bubble_sort2(nums):
    for i in range(len(nums) - 1):
        for j in range(1, len(nums) - i):
            if nums[j] < nums[j - 1]:
                nums[j], nums[j - 1] = nums[j - 1], nums[j]
        print(nums)
    return nums


def bubbleSort(arr):
    for i in range(1, len(arr)):
        for j in range(0, len(arr)-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        print(arr)
    return arr


if __name__ == '__main__':
    print(test_unit([23, 11, 7, 29, 33, 59, 8, 20, 9, 3, 2, 6, 10, 44, 83, 28, 5, 1, 0, 36], bubble_sort))
