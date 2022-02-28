# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

from leetcode.common import Node


def del_reserve_n_node(node, n):
    """
    删除倒数第 N 个节点
    :param node:
    :param n:
    :return:
    """
    if not node:
        return None

    if n < 1:
        return node

    h = head
    slow = head
    fast = head
    for i in range(n):
        slow = slow.next

    dum = None
    while slow:
        slow = slow.next
        dum = fast
        fast = fast.next
    dum.next = fast.next
    return h

node3 = Node(5, None)
node4 = Node(4, node3)
node5 = Node(3, node4)
node6 = Node(2, node5)
node7 = Node(1, node6)

head = del_reserve_n_node(node7, 2)
while head:
    print(head.value)
    head = head.next

