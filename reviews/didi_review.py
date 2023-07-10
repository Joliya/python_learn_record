"""
二维数组， n * n， 只能往 下、下左、下右。
1、求从第一行的某个位置 到最后一行的某个位置的路径之和最大值是多少。
2、如果要求 必须经过 坐标 x,y ， 那么算法怎么改进

1 2 3 4 5
1 2 3 4 5
1 2 3 4 5
1 2 3 4 5
1 2 3 4 5


1 2 3 4
1 2 3 4
1 2 3 4
1 2 3 4
"""


def max_path(nums):

    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0][0]
    # 初始化一个 n + 1 * n + 1 的数组，用来存放路径上的数字之和, 最外层包一圈，是为了减少判断，不影响最终结果
    dp = [[0] * n for _ in range(n)]
    #  0，0的位置的值为 nums 的第一个值
    for i in range(n):
        dp[0][i] = nums[0][i]

    for i in range(n):
        for j in range(n):
            # 如果是第一列，只能往下、右下走
            if j == 0:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j+1]) + nums[i][j]
            elif j == n - 1:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - 1]) + nums[i][j]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-1], dp[i-1][j+1]) + nums[i][j]
    # print(dp)
    return max(dp[n - 1])


def min_path(nums):

    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0][0]
    # 初始化一个 n + 1 * n + 1 的数组，用来存放路径上的数字之和, 最外层包一圈，是为了减少判断，不影响最终结果
    dp = [[0] * n for _ in range(n)]
    #  0，0的位置的值为 nums 的第一个值
    for i in range(n):
        dp[0][i] = nums[0][i]

    for i in range(n):
        for j in range(n):
            # 如果是第一列，只能往下、右下走
            if j == 0:
                dp[i][j] = min(dp[i-1][j], dp[i-1][j+1]) + nums[i][j]
            elif j == n - 1:
                dp[i][j] = min(dp[i - 1][j], dp[i - 1][j - 1]) + nums[i][j]
            else:
                dp[i][j] = min(dp[i-1][j], dp[i-1][j-1], dp[i-1][j+1]) + nums[i][j]
    # print(dp)
    return min(dp[n - 1])


def max_path_dfs(nums):

    dirs = [(1, 0), (1, -1), (1, 1)]
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0][0]
    def dfs(row, col):
        if row == n - 1:
            return nums[row][col]
        for r, c in dirs:
            row_new, col_new = r + row, c + col
            if 0 < row_new < n and 0 < col_new < n:
                return dfs(row_new, col_new) + nums[row][col]

    max_ans = 0
    for i in range(n):
        max_ans = max(max_ans, dfs(0, i))
    return max_ans


def max_path_dfs_xy(nums, x, y):

    dirs = [(1, 0), (1, -1), (1, 1)]
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0][0]

    def dfs(row, col, pass_xy):
        if row == x and col != y:
            return 0, False

        if row == n - 1:
            return nums[row][col], True
        cur_dfs_max = 0
        for r, c in dirs:
            row_new, col_new = r + row, c + col
            if 0 <= row_new < n and 0 <= col_new < n:
                # 每次递归结束后拿当前递归的最大值
                value, pass_xy = dfs(row_new, col_new, pass_xy)
                value1 = nums[row][col] if pass_xy else 0
                cur_dfs_max = max(value + value1, cur_dfs_max)
        return cur_dfs_max, True

    max_ans = 0
    for i in range(n):
        pass_xy = True
        nnn, _ = dfs(0, i, pass_xy)
        max_ans = max(max_ans, nnn)
    # pass_xy = True
    # nnn, _ = dfs(0, n - 1, pass_xy)
    # max_ans = max(max_ans, nnn)
    return max_ans


if __name__ == '__main__':
    n = 5
    nums = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            nums[i][j] = j + 1
    print("原始数组", nums)

    print("最长路径", max_path(nums))
    print("最长路径", max_path_dfs(nums))

    for i in range(n):
        for j in range(n):
            print(max_path_dfs_xy(nums, i, j), i, j)
    # print(max_path_dfs_xy(nums, 3, 0), 3, 0)

