# -*- encoding: utf-8 -*-
"""
删除列表重复元素
列表已经正向有序
"""

from __future__ import absolute_import, unicode_literals

from leetcode.common import Node


def delete_repeat_node(node: Node):
    """
    删除链表重复节点
    :param node:
    :return:
    """
    head = node
    while(node.next != None):
        if node.value == node.next.value:
            node.next = node.next.next
        else:
            node = node.next
    return head


node1 = Node(20, None)
node2 = Node(20, node1)
node3 = Node(20, node2)
node4 = Node(12, node3)
node5 = Node(9, node4)
node6 = Node(9, node5)
node7 = Node(1, node6)


node = delete_repeat_node(node7)
while(node):
    print(node.value)
    node = node.next

