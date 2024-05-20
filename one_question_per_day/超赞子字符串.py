"""
@file: 超赞子字符串.py
@time: 2024/5/20 10:09
@desc:
给你一个字符串 s 。请返回 s 中最长的 超赞子字符串 的长度。

「超赞子字符串」需满足满足下述两个条件：

该字符串是 s 的一个非空子字符串
进行任意次数的字符交换后，该字符串可以变成一个回文字符串


示例 1：

输入：s = "3242415"
输出：5
解释："24241" 是最长的超赞子字符串，交换其中的字符后，可以得到回文 "24142"
示例 2：

输入：s = "12345678"
输出：1
示例 3：

输入：s = "213123"
输出：6
解释："213123" 是最长的超赞子字符串，交换其中的字符后，可以得到回文 "231132"
示例 4：

输入：s = "00"
输出：2


提示：

1 <= s.length <= 10^5
s 仅由数字组成
"""


class Solution:
    def longestAwesome(self, s: str) -> int:
        s_len = len(s)
        if s_len == 0:
            return 0
        if s_len == 1:
            return s_len
        max_awe = 1
        low, fast = 0, 1
        while fast < len(s):
            if self.is_back_str(s[low: fast + 1]):
                cur_awe = fast - low + 1
                if cur_awe > max_awe:
                    max_awe = cur_awe
                fast += 1
            else:
                low += 1
                fast += 1
        return max_awe

    def is_back_str(self, s: str) -> bool:
        s_len = len(s)
        if s_len == 0:
            return False
        if s_len == 1:
            return True
        s_dict = {}
        for i in s:
            if i in s_dict:
                s_dict[i] += 1
            else:
                s_dict[i] = 1
        odd_count = 0
        for i in s_dict.values():
            if i % 2 != 0:
                odd_count += 1
        if odd_count > 1:
            return False
        return True


class Solution1:
    def longestAwesome(self, s: str) -> int:
        """leetcode 官方解法"""
        n = len(s)
        prefix = {0: -1}
        ans, sequence = 0, 0

        for j in range(n):
            digit = ord(s[j]) - ord("0")
            sequence ^= (1 << digit)
            if sequence in prefix:
                ans = max(ans, j - prefix[sequence])
            else:
                prefix[sequence] = j
            for k in range(10):
                if sequence ^ (1 << k) in prefix:
                    ans = max(ans, j - prefix[sequence ^ (1 << k)])

        return ans


if __name__ == '__main__':
    print(Solution().longestAwesome("3242415"))
