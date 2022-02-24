# -*- encoding: utf-8 -*-
"""
链表反转
"""

from __future__ import absolute_import, unicode_literals


class Node:

    def __init__(self, value, node):
        self.value = value
        self.next = node

    def __str__(self):
        return f"value: {self.value}"


def reverse_list(node):
    """
    反转列表
    :param node:
    :return:
    """

    if not node or not node.next:
        return node
    h = None
    m = node
    while(m):
        t = m.next
        m.next = h
        h = m
        m = t
    return h




node1 = Node(50, None)
node2 = Node(20, node1)
node3 = Node(15, node2)
node4 = Node(12, node3)
node5 = Node(9, node4)
node6 = Node(6, node5)
node7 = Node(1, node6)

node = node7
while(node):
    print(node.value)
    node = node.next

print("__________________")
node = reverse_list(node7)
while(node):
    print(node.value)
    node = node.next
