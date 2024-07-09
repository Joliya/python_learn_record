"""
@file: 最小化曼哈顿距离.py
@time: 2024/7/9 19:04
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

"""
from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
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
