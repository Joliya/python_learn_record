"""
二分排序算法

主要思想：
每次取中间的数，然后插入到合适的位置
"""
from leetcode.base_sort.test_unit import test_unit


def two_split_sort(nums):
    """
    二分排序算法
    :param nums:
    :return:
    """
    for i in range(1, len(nums)):
        left, right = 0, i - 1
        temp = nums[i]
        # 根据中位查找， 找到当前i位置的数应该放在哪个 left 下标后面
        while left <= right:
            mid = (left + right) // 2
            if temp < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # 将已经有序部分中 大于 i 位置的数据的数据后移
        for j in reversed(range(left, i)):
            nums[j + 1] = nums[j]
        # 空出来的 left 位置即为实际i位置的数要插入的地方
        nums[left] = temp
    return nums


if __name__ == '__main__':
    print(test_unit([23, 11, 7, 29, 33, 59, 8, 20, 9, 3, 2, 6, 10, 44, 83, 28, 5, 1, 0, 36], two_split_sort))
