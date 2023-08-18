"""


给定一个经过编码的字符串，返回它解码后的字符串
输入：s = "30[a]2[bc]"
输出："aaabcbc"

输入：s = "3[a23333[c]]"
输出："accaccacc"
"""

from __future__ import absolute_import, unicode_literals


def parse_str(s):
    result = ""
    stack = list()
    cur_str = ""
    cur_num_str = ""
    for i in s:
        if i != "]":
            stack.append(i)
        else:
            flag = True
            pass_left = False
            while flag:
                pop_char = stack.pop() if stack else None
                if not pop_char:
                    flag = False
                elif pop_char != "[" and not pop_char.isdigit() and not pass_left:
                    cur_str = f"{pop_char}{cur_str}"
                elif pop_char.isdigit():
                    cur_num_str += pop_char
                elif pop_char == "[":
                    pass_left = True
                    continue
                else:
                    stack.append(pop_char)
                    flag = False
            cur_str = int(cur_num_str) * cur_str
            cur_num_str = ""
            if "[" not in stack:
                result += cur_str
                cur_str = ""
                cur_num_str = ""
    return result


if __name__ == '__main__':
    print(parse_str("3[a]2[bc]"))
    print(parse_str("3[a2[c]]"))





