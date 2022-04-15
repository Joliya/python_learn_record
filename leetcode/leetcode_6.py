# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals


# 将一个给定字符串 s 根据给定的行数 numRows ，以从上往下、从左到右进行 Z 字形排列。
#
#  比如输入字符串为 "PAYPALISHIRING" 行数为 3 时，排列如下：
#
#
# P   A   H   N
# A P L S I I G
# Y   I   R
#
#  之后，你的输出需要从左往右逐行读取，产生出一个新的字符串，比如："PAHNAPLSIIGYIR"。
#
#  请你实现这个将字符串进行指定行数变换的函数：
#
#
# string convert(string s, int numRows);
#
#
#
#  示例 1：
#
#
# 输入：s = "PAYPALISHIRING", numRows = 3
# 输出："PAHNAPLSIIGYIR"
#
# 示例 2：
#
#
# 输入：s = "PAYPALISHIRING", numRows = 4
# 输出："PINALSIGYAHRPI"
# 解释：
# P     I    N
# A   L S  I G
# Y A   H R
# P     I
#
#
#  示例 3：
#
#
# 输入：s = "A", numRows = 1
# 输出："A"
#
#
#
#
#  提示：
#
#
#  1 <= s.length <= 1000
#  s 由英文字母（小写和大写）、',' 和 '.' 组成
#  1 <= numRows <= 1000
#
#  Related Topics 字符串 👍 1652 👎 0


# leetcode submit region begin(Prohibit modification and deletion)
class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        if numRows == 1:
            return s
        res = [''] * numRows
        index, step = 0, 1
        for x in s:
            res[index] += x
            if index == 0:
                step = 1
            elif index == numRows - 1:
                step = -1
            index += step
        return ''.join(res)
# leetcode submit region end(Prohibit modification and deletion)


class Solution1(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        if numRows == 1:
            return s
        res = [""] * numRows
        step = 0
        down = True
        for i in s:
            res[step] = res[step] + i
            if step == numRows - 1:
                down = False
            if step == 0:
                down = True
            if down:
                step += 1
            else:
                step -= 1
        return "".join(res)


s = "PAYPALISHIRING"
# P     I    N
# A   L S  I G
# Y A   H R
# P     I
numRows = 4
print(Solution1().convert(s, numRows))
print("PINALSIGYAHRPI")

