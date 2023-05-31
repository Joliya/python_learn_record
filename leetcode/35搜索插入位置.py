"""
给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。如果目标值不存在于数组中，返回它将会被按顺序插入的位置。

请必须使用时间复杂度为 O(log n) 的算法。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/search-insert-position
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""



# 二分查找， 关键在于 mid 的定义， 二分查找很容易引起死循环
class Solution(object):
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        if len(nums) == 0:
            return 0
        l = 0
        r = len(nums) - 1
        if nums[r] < target:
            return len(nums)
        while l < r:
            mid = (l + r) / 2
            if nums[mid] < target:
                l = mid + 1
            else:
                r = mid
        return l
