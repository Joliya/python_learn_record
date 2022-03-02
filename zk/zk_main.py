# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

import  simplejson as json

from zk.zk_manager import ZkClient

if __name__ == "__main__":

    zk_client = ZkClient()
    print(zk_client.create_node_shunxu())
    children = zk_client.get_children("/rpc")
    print(children)
    data, _ = zk_client.get_node_by_path("/rpc/" + children[1])
    print(json.loads(data))

    data, _ = zk_client.get_node_by_path("/rpc/" + children[0])
    print(json.loads(data))
    # result = zk_client.create_node("/a/b", "zhangsan")
    # print(result)
    #
    # x = zk_client.get_node_by_path("/a/b")
    # print(x)
