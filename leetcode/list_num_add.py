# -*- encoding: utf-8 -*-
"""
两数相加
"""

from __future__ import absolute_import, unicode_literals


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

"""
输入：l1 = [2,4,3], l2 = [5,6,4]
输出：[7,0,8]
解释：342 + 465 = 807.
示例 2：

输入：l1 = [0], l2 = [0]
输出：[0]
示例 3：

输入：l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
输出：[8,9,9,9,0,0,0,1]
"""
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        def do(cur, node):
            div_num = cur / 10
            yu_num = cur % 10
            node.next = ListNode(yu_num, None)
            node = node.next
            return div_num, node


        node = ListNode()
        dummy = node
        div_num = 0
        while (l1 and l2):
            cur = l1.val + l2.val + div_num
            div_num, node = do(cur, node)
            l1 = l1.next
            l2 = l2.next

        while l2:
            value = l2.val + div_num
            div_num, node = do(value, node)
            l2 = l2.next
        while l1:
            value = l1.val + div_num
            div_num, node = do(value, node)
            l1 = l1.next
        if div_num:
            node.next = ListNode(div_num, None)
        return dummy.next
