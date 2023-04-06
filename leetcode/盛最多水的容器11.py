"""
给定一个长度为 n 的整数数组 height 。有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i]) 。

找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

返回容器可以储存的最大水量。

说明：你不能倾斜容器。

"""



# 太慢了。 执行超时。。。。 艹
class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        max_list = []
        for i in range(len(height)):
            l = []
            for i in range(len(height)):
                l.append(0)
            max_list.append(l)
        max_list[0][0] = 123
        for idx, i in enumerate(height):
            for idx2, i2 in enumerate(height):
                if idx2 < idx:
                    continue
                max_list[idx][idx2] = abs(idx2 - idx) * min(i, i2)
        return max([max(j) for j in max_list])


# 双指针， 短板移动向内移动才有机会面积更大， 长板往内移动碰到短板一定面积变小
class Solution2(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        max_len = len(height)
        if max_len < 2:
            return 0
        i = 0
        j = max_len - 1
        max_area = 0
        while i < j:
            area = (j - i) * min(height[i], height[j])
            if area > max_area:
                max_area = area
            if height[i] > height[j]:
                j -= 1
            else:
                i += 1
        return max_area


print(Solution().maxArea([1,8,6,2,5,4,8,3,7]))
