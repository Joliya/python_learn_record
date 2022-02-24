# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals


class Node:

    def __init__(self, value, node):
        self.value = value
        self.next = node

    def __str__(self):
        return f"value: {self.value}"


def merge_list(node_1, node_2):
    """
    合并列表
    :param node_1:
    :param node_2:
    :return:
    """

    if not node_1 and not node_2:
        return None

    if not node_1:
        return node_2
    if not node_2:
        return node_1
    if node_1.value > node_2.value:
        node_2.next = merge_list(node_1, node_2.next)
        return node_2
    else:
        node_1.next = merge_list(node_1.next, node_2)
        return node_1


def merge_list_for(node_1, node_2):
    """
    for 循环
    :param node_1:
    :param node_2:
    :return:
    """
    if not node_1 and not node_2:
        return None

    if not node_1:
        return node_2
    if not node_2:
        return node_1

    new_node = Node(0, None)
    head = new_node
    while(node_1 and node_2):
        if node_1.value > node_2.value:
            new_node.next = node_2
            node_2 = node_2.next
        else:
            new_node.next = node_1
            node_1 = node_1.next
        new_node = new_node.next

    if node_1:
        new_node.next = node_1
    if node_2:
        new_node.next = node_2

    return head.next



node1 = Node(50, None)
node2 = Node(20, node1)
node3 = Node(15, node2)
node4 = Node(12, node3)
node5 = Node(9, node4)
node6 = Node(6, node5)
node7 = Node(1, node6)



node8 = Node(40, None)
node9 = Node(23, node8)
node10 = Node(19, node9)
node11 = Node(14, node10)
node12 = Node(6, node11)
node13 = Node(3, node12)
node14 = Node(2, node13)

#
# node = merge_list(node14, node7)
node = merge_list_for(node14, node7)

while(node):

    print(node.value)
    node = node.next



