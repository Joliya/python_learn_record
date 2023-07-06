"""
二维数组， n * n， 只能往 下、下左、下右。

1 2 3 4 5
1 2 3 4 5
1 2 3 4 5
1 2 3 4 5
1 2 3 4 5
"""


def max_path(nums):
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0][0]
    # 初始化一个 n + 1 * n + 1 的数组，用来存放路径上的数字之和, 最外层包一圈，是为了减少判断，不影响最终结果
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    #  0，0的位置的值为 nums 的第一个值
    dp[0][0] = nums[0][0]

    for i in range(n):
        for j in range(n):
            # 如果是第一列，只能往下、右下走
            if j == 0:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j+1]) + nums[i][j]
            elif j == n - 1:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - 1]) + nums[i][j]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-1], dp[i-1][j+1]) + nums[i][j]
    print(dp)
    return max(dp[n - 1])


if __name__ == '__main__':
    n = 5
    nums = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            nums[i][j] = j + 1
    print("原始数组", nums)

    print(max_path(nums))
