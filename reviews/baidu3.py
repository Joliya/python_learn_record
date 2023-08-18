"""

"""

from __future__ import absolute_import, unicode_literals


def solution(s: str):
    """

    返回字符串对应数字
    :param s:
    :return:
    """
    col_name = s.upper()
    result = 0
    for c_name in col_name:
        result = result * 26 + (ord(c_name) - ord('A')) + 1
    return result





class Solution:
    def insert(self, intervals, newInterval):
        if not intervals:
            return [newInterval]
        if len(intervals) == 1:
            return [[min(intervals[0][0], newInterval[0])], max(intervals[0][1], newInterval[1])]
        result = []
        merge_list = []
        new_left, new_right = newInterval
        for i_left, i_right in intervals:
            # 1  5
            # 2  3
            if i_right < new_left:
                result.append([i_left, i_right])
                continue
            elif i_left > new_right:
                if merge_list:
                    interval = [min(merge_list[0][0], new_left), max(merge_list[-1][1], new_right)]
                else:
                    interval = newInterval
                result.append(interval)
                result.append([i_left, i_right])
            elif new_left > i_left and new_right < i_right:
                result.append([i_left, i_right])
            else:
                merge_list.append([i_left, i_right])

        return result


if __name__ == '__main__':
    intervals = [[1,5]]
    new_intervals = [2,7]
    Solution().insert(intervals, new_intervals)
