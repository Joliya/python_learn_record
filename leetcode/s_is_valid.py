# 给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。
#
#  有效字符串需满足：
#
#
#  左括号必须用相同类型的右括号闭合。
#  左括号必须以正确的顺序闭合。
#
#
#
#
#  示例 1：
#
#
# 输入：s = "()"
# 输出：true
#
#
#  示例 2：
#
#
# 输入：s = "()[]{}"
# 输出：true
#
#
#  示例 3：
#
#
# 输入：s = "(]"
# 输出：false
#
#
#  示例 4：
#
#
# 输入：s = "([)]"
# 输出：false
#
#
#  示例 5：
#
#
# 输入：s = "{[]}"
# 输出：true
#
#
#
#  提示：
#
#
#  1 <= s.length <= 10⁴
#  s 仅由括号 '()[]{}' 组成
#
#  Related Topics 栈 字符串 👍 2723 👎 0


# leetcode submit region begin(Prohibit modification and deletion)
class Solution(object):

    def isValid(self, s: str):
        """
        :type s: str
        :rtype: bool
        """
        s_len = len(s)
        if s_len % 2 != 0:
            return False
        s_dict = {
            '(': ")",
            '{': "}",
            '[': "]",
        }
        st = ['?']
        for i in s:
            if i in s_dict:
                st.append(i)
            elif s_dict[st.pop()] != i:
                return False
        return len(st) == 1
# leetcode submit region end(Prohibit modification and deletion)

# s = "{{{}}}(([[[]]"
# s = "[[[{{{}}}]]]()()()"
s = "{}{}{}{}[][][]{}{}{}()()()(){([])}"
print(Solution().isValid(s))
