"""
给定一个m x n 二维字符网格board 和一个字符串单词word 。如果word 存在于网格中，返回 true ；否则，返回 false 。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

例如，在下面的 3×4 的矩阵中包含单词 "ABCCED"（单词中的字母已标出）。

A B C E
S F C S
A D E E

ABCCED


输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
输出：true

输入：board = [["a","b"],["c","d"]], word = "abcd"
输出：false
"""
from typing import List


class Solution1(object):
    def exist(self, board: List[List[str]], word: str):
        """
        暴力、dfs，额外开辟一个 visited 访问过的节点的数组空间
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def _check(i: int, j: int, k: int):
            if board[i][j] != word[k]:
                return False
            if k == len(word) - 1:
                return True

            visited.add((i, j))
            result = False
            for addi, addj in directions:
                newi, newj = i + addi, j + addj
                if i_min <= newi < i_max and j_min <= newj < j_max:
                    if (newi, newj) in visited:
                        continue
                    if _check(newi, newj, k + 1):
                        result = True
                        break
            visited.remove((i, j))
            return result

        i_max, j_max = len(board), len(board[0])
        if i_max == 0:
            return False
        i_min, j_min = 0, 0
        visited = set()
        for i in range(i_max):
            for j in range(j_max):
                if _check(i, j, 0):
                    return True
        return False


class Solution2:
    def exist(self, board: List[List[str]], word: str) -> bool:
        """
        也是暴力，不过不用额外开辟 已经访问过的位置的数组，而是把访问过的数组位置 改为特殊字符 空字符串
        :param board:
        :param word:
        :return:
        """
        def dfs(i, j, k):
            # 1、越界情况  2、当前位置元素和 word 对应个数的元素不一致
            if not 0 <= i < len(board) or not 0 <= j < len(board[0]) or board[i][j] != word[k]:
                return False
            # 如果 k 已经和 word 的长度一致，说明已经完全匹配
            if k == len(word) - 1:
                return True
            # 当前位置字符 和 word 对应位置字符匹配上后
            board[i][j] = ''
            # 深度递归
            res = dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1) or dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1)
            board[i][j] = word[k]
            return res

        for i in range(len(board)):
            for j in range(len(board[0])):
                if dfs(i, j, 0):
                    return True
        return False


class Solution3(object):
    def exist(self, board: List[List[str]], word: str):
        """
        暴力、dfs， 不额外开辟数组空间
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def _check(i: int, j: int, k: int):
            if board[i][j] != word[k]:
                return False
            if k == len(word) - 1:
                return True

            board[i][j] = ""
            result = False
            for addi, addj in directions:
                newi, newj = i + addi, j + addj
                if i_min <= newi < i_max and j_min <= newj < j_max:
                    # if board[i][j] == "":
                    #     continue
                    if _check(newi, newj, k + 1):
                        result = True
                        break
            board[i][j] = word[k]
            return result

        i_max, j_max = len(board), len(board[0])
        if i_max == 0:
            return False
        i_min, j_min = 0, 0
        for i in range(i_max):
            for j in range(j_max):
                if _check(i, j, 0):
                    return True
        return False


if __name__ == '__main__':
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    word = "ABCCED"
    print(Solution1().exist(board, word))
    print(board)
    print(Solution2().exist(board, word))
    print(board)
    print(Solution3().exist(board, word))
    print(board)
