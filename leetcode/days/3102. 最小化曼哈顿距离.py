"""
@file: 3102. 最小化曼哈顿距离.py
@time: 2024/8/16 20:44
@desc:


给你一个下标从 0 开始的数组 points ，它表示二维平面上一些点的整数坐标，其中 points[i] = [xi, yi] 。

两点之间的距离定义为它们的
曼哈顿距离
。

请你恰好移除一个点，返回移除后任意两点之间的 最大 距离可能的 最小 值。



示例 1：

输入：points = [[3,10],[5,15],[10,2],[4,4]]
输出：12
解释：移除每个点后的最大距离如下所示：
- 移除第 0 个点后，最大距离在点 (5, 15) 和 (10, 2) 之间，为 |5 - 10| + |15 - 2| = 18 。
- 移除第 1 个点后，最大距离在点 (3, 10) 和 (10, 2) 之间，为 |3 - 10| + |10 - 2| = 15 。
- 移除第 2 个点后，最大距离在点 (5, 15) 和 (4, 4) 之间，为 |5 - 4| + |15 - 4| = 12 。
- 移除第 3 个点后，最大距离在点 (5, 15) 和 (10, 2) 之间的，为 |5 - 10| + |15 - 2| = 18 。
在恰好移除一个点后，任意两点之间的最大距离可能的最小值是 12 。
示例 2：

输入：points = [[1,1],[1,1],[1,1]]
输出：0
解释：移除任一点后，任意两点之间的最大距离都是 0 。
https://leetcode.cn/problems/minimize-manhattan-distances/solutions/2829782/zui-xiao-hua-man-ha-dun-ju-chi-by-leetco-dipa/



提示：「曼哈顿距离与切比雪夫距离的相互转化」
"""
from typing import List


from sortedcontainers import SortedList


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        # 提示：「曼哈顿距离与切比雪夫距离的相互转化」
        sx = SortedList(p[0] - p[1] for p in points)
        sy = SortedList(p[0] + p[1] for p in points)
        res = float('inf')
        for p in points:
            sx.remove(p[0] - p[1])
            sy.remove(p[0] + p[1])
            res = min(res, max(sx[-1] - sx[0], sy[-1] - sy[0]))
            sx.add(p[0] - p[1])
            sy.add(p[0] + p[1])
        return res


class Solution2:
    """
    思路与算法
    根据方法一可以知道，假设目前已知构成最大曼哈顿距离的两点分别为 A,B，此时最有选择必然是去掉 A 或者 B，此时再次计算去掉 A 或者 B 后的最大曼哈顿距离，取二者的最小值返回即可。
    """
    def minimumDistance(self, points: List[List[int]]) -> int:
        def remove(arr: List[tuple], i: int) -> int:
            n = len(arr)
            if arr[0][1] == i:
                return arr[n - 1][0] - arr[1][0]
            elif arr[-1][1] == i:
                return arr[n - 2][0] - arr[0][0]
            else:
                return arr[-1][0] - arr[0][0]

        n = len(points)
        sx = [(x - y, i) for i, (x, y) in enumerate(points)]
        sy = [(x + y, i) for i, (x, y) in enumerate(points)]
        sx.sort()
        sy.sort()
        maxVal1 = sx[-1][0] - sx[0][0]
        maxVal2 = sy[-1][0] - sy[0][0]
        res = float('inf')
        if maxVal1 >= maxVal2:
            i, j = sx[0][1], sx[-1][1]
            # 去掉 i 后的最大曼哈顿距离
            res = min(res, max(remove(sx, i), remove(sy, i)))
            # 去掉 j 后的最大曼哈顿距离
            res = min(res, max(remove(sx, j), remove(sy, j)))
        else:
            i, j = sy[0][1], sy[-1][1]
            # 去掉 i 后的最大曼哈顿距离
            res = min(res, max(remove(sx, i), remove(sy, i)))
            # 去掉 j 后的最大曼哈顿距离
            res = min(res, max(remove(sx, j), remove(sy, j)))
        return res
