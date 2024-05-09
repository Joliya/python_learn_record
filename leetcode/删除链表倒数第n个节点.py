# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

from leetcode.common import Node


def del_reserve_n_node(head, n):
    """
    删除倒数第 N 个节点
    :param head:
    :param n:
    :return:
    """
    if not head:
        return None

    if n < 1:
        return head

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


def del_reserve_n_node2(node, n):
    if not node:
        return None

    stack = []
    head = node
    while node:
        stack.append(node)
        node = node.next
    count = -1
    cur_node = None
    while count != n:
        cur_node = stack.pop()
        count += 1
    if cur_node:
        cur_node.next = cur_node.next.next
    return head


node3 = Node(5, None)
node4 = Node(4, node3)
node5 = Node(3, node4)
node6 = Node(2, node5)
node7 = Node(1, node6)

head = del_reserve_n_node(node7, 2)
while head:
    print(head.value)
    head = head.next

