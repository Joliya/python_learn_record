"""
@file: Trie.py
@time: 2024/4/1 19:39
@desc: trie 树， 是一种用空间换时间的数据结构，用于快速检索字符串，根结点不存储内容，每个结点有若干子结点，
每个结点的子结点的值不相同，从根结点到某一结点，路径上经过的字符连接起来，为该结点对应的字符串， 通常用于搜索提示，字符串结尾标记为结束符
详解内容：https://zhuanlan.zhihu.com/p/340228499
"""
import unittest


class TrieNode:
    def __init__(self):
        self.is_key = False  # 标志，False：不是字符串结尾，True：是字符串结尾
        self.children = [None] * 26  # 指向子节点的列表


# 插入字符串到 Trie 树中
def insert(s, root):
    p = root
    for c in s:
        index = ord(c) - ord('a')
        if not p.children[index]:  # 如果没有对应子节点，创建新节点
            p.children[index] = TrieNode()
        p = p.children[index]
    p.is_key = True  # 字符串结尾标志置为 True


# 在 Trie 树中检索字符串
def search(s, root):
    p = root
    for c in s:
        index = ord(c) - ord('a')
        if not p.children[index]:  # 如果子节点不存在，说明字符串不在 Trie 树中
            return False
        p = p.children[index]
    return p.is_key  # 如果最后的节点标志为 True，说明找到了完整的字符串


# 在 Trie 树中删除字符串
def remove(s, root):
    if not search(s, root):  # 如果字符串不在 Trie 树中，直接返回
        return
    p = root
    stack = []  # 存储路径上节点的栈
    for c in s:
        index = ord(c) - ord('a')
        stack.append((p, index))  # 存储当前节点和对应子节点的索引
        p = p.children[index]
    p.is_key = False  # 将字符串结尾的节点标志置为 False

    # 回溯删除不再需要的���点
    while stack:
        node, idx = stack.pop()
        if node.children[idx].is_key or any(node.children[idx].children):  # 如果是其他字符串的结尾或有子节点，停止删除
            break
        node.children[idx] = None  # 删除指向子节点的引用


# 测试用例
class TestTrie(unittest.TestCase):
    def setUp(self):
        self.root = TrieNode()

    def test_insert_search(self):
        insert("apple", self.root)
        self.assertTrue(search("apple", self.root))  # 确保 "apple" 已插入
        self.assertFalse(search("app", self.root))   # "app" 不是完整的字符串
        print(self.root)

    def test_insert_remove_search(self):
        insert("apple", self.root)
        insert("app", self.root)
        self.assertTrue(search("app", self.root))    # 确保 "app" 已插入

        remove("apple", self.root)
        self.assertTrue(search("app", self.root))    # "app" 仍在 Trie 中
        self.assertFalse(search("apple", self.root)) # "apple" 已被移除

    def test_remove_nonexistent(self):
        remove("nonexistent", self.root)  # 尝试移除不存在的字符串
        self.assertFalse(search("nonexistent", self.root))  # 确保没有错误发生


# 运行测试用例
if __name__ == '__main__':
    unittest.main()
