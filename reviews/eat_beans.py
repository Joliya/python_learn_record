# -*- encoding: utf-8 -*-
"""
魔镜公司 2022-03-08 面试题
"""

from __future__ import absolute_import, unicode_literals


"""
一个小朋友吃n颗豆子，每次只能吃 1 个或者 2个， 但不能连续吃两个，有多少种方式吃完N颗豆子

f(1) = 1
f(2) = 2
f(3) = 3
f(4) = 4
f(5) = 6
f(6) = 9
f(7) = 13
状态转移方程    f(n) = f(n-1) + f(n-3)
"""


def eat_beans(n):
    """
    吃豆子
    :param n: 豆子总数
    :return:
    """
    assert n > 0, "n 必须是大于 0 的数"
    if n < 5:
        return n
    f = [0] * (n + 1)
    for i in range(5):
        f[i] = i
    for i in range(5, n+1):
        f[i] = f[i-1] + f[i-3]
    return f[-1]


if __name__ == '__main__':
    for i in range(3, 10):
        print(eat_beans(i))

