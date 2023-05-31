"""
写一个函数，输入 n ，求斐波那契（Fibonacci）数列的第 n 项（即 F(N)）。斐波那契数列的定义如下：

F(0) = 0, F(1)= 1
F(N) = F(N - 1) + F(N - 2), 其中 N > 1.
斐波那契数列由 0 和 1 开始，之后的斐波那契数就是由之前的两数相加而得出。

答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/fei-bo-na-qi-shu-lie-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。


输入：n = 2
输出：1


输入：n = 5
输出：5
"""


class Solution(object):
    def fib(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n == 0:
            return 0
        if n == 1:
            return 1
        f = [0] * (n + 1)
        f[1] = 1
        for i in range(2, n + 1):
            f[i] = f[i - 1] + f[i - 2]
            f[i] %= 1000000007
        return f[n]


class Solution2(object):
    def fib(self, n):
        """
        :type n: int
        :rtype: int
        """
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b
            a %= 1000000007
        return a


if __name__ == '__main__':
    print(Solution().fib(2))
    print(Solution().fib(5))
    print(Solution().fib(45))
