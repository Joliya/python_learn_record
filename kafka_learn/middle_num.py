# -*- encoding: utf-8 -*-
"""
寻找两个正序数组的中位数
"""

from __future__ import absolute_import, unicode_literals


# 给定两个大小分别为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。请你找出并返回这两个正序数组的 中位数 。
#
#  算法的时间复杂度应该为 O(log (m+n)) 。
#
#
#
#  示例 1：
#
#
# 输入：nums1 = [1,3], nums2 = [2]
# 输出：2.00000
# 解释：合并数组 = [1,2,3] ，中位数 2
#
#
#  示例 2：
#
#
# 输入：nums1 = [1,2], nums2 = [3,4]
# 输出：2.50000
# 解释：合并数组 = [1,2,3,4] ，中位数 (2 + 3) / 2 = 2.5
#
#
#
#
#
#
#  提示：
#
#
#  nums1.length == m
#  nums2.length == n
#  0 <= m <= 1000
#  0 <= n <= 1000
#  1 <= m + n <= 2000
#  -10⁶ <= nums1[i], nums2[i] <= 10⁶
#
#  Related Topics 数组 二分查找 分治 👍 5079 👎 0


# leetcode submit region begin(Prohibit modification and deletion)
class Solution(object):
    def findMedianSortedArrays(self, nums1: list, nums2: list):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        nums2.extend(nums1)
        if not nums2:
            return 0
        nums2.sort(key=lambda x: x)
        print(nums2)
        m = len(nums2)
        if m % 2 != 0:
            return nums2[int((m - 1) / 2)]
        return (nums2[int((m / 2))] + nums2[int((m / 2 - 1))]) / 2

    def findMedianSortedArrays2(self, nums1: list, nums2: list):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        m = len(nums1)
        n = len(nums2)
        l = m + n
        if l % 2 == 0:
            middle = l / 2
        else:
            middle = (l - 1) / 2

        i = 0
        j = 0
        left = 0
        right = 0
        for x in range(int(middle) + 1):
            left = right
            if i < m and nums2[j] > nums1[i]:
                right = nums1[i]
                i += 1
            else:
                right = nums2[j]
                if j < n - 1:
                    j += 1
        print(left, right)
        if l % 2 == 0:
            return (left + right) / 2.0
        return right


# leetcode submit region end(Prohibit modification and deletion)

nums1 = [1]
nums2 = [3,4]
print(Solution().findMedianSortedArrays2(nums1, nums2))
