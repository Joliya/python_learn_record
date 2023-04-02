# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

# 给你一个字符串 s，找到 s 中最长的回文子串。
#
#
#
#  示例 1：
#
#
# 输入：s = "babad"
# 输出："bab"
# 解释："aba" 同样是符合题意的答案。
#
#
#  示例 2：
#
#
# 输入：s = "cbbd"
# 输出："bb"
#
#
#
#
#  提示：
#
#
#  1 <= s.length <= 1000
#  s 仅由数字和英文字母组成
#
#  Related Topics 字符串 动态规划 👍 5072 👎 0
class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        length = len(s)
        if length < 1:
            return ""
        if length == 1:
            return s
        low = 0
        l = 0
        for i in range(length):
            for j in range(i + 1, length + 1):
                if self.is_rome(s[i: j]):
                    if j - i > l:
                        low = i
                        l = j - i
        return s[low: low + l]

    def is_rome(self, rome_str):
        """
        是否是回文字符串
        :param rome_str:
        :return:1,2,3,4,5,6
        """
        length = len(rome_str)
        index = int(length / 2)
        for i in range(index):
            if rome_str[i] != rome_str[-(i + 1)]:
                return False
        return True


if __name__ == '__main__':
    s = "abababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababa"
    print(Solution().longestPalindrome(s))

