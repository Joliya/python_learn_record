# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

from kazoo.client import KazooClient
import simplejson as json


class ZkClient:

    def __init__(self):

        self._zk_client = KazooClient(hosts="192.168.102.177:2181")
        self._zk_client.start()

    def create_node(self, path, value):
        return self._zk_client.create(path, value.encode())

    def get_node_by_path(self, path):

        return self._zk_client.get(path)

    def create_node_shunxu(self):
        self._zk_client.ensure_path("/rpc")
        addr1 = json.dumps({
            "host": "127.0.0.1",
            "port": 8001
        })
        addr2 = json.dumps({
            "host": "127.0.0.1",
            "port": 8002
        })
        # 创建节点并在节点保存数据 ephemeral表示是否是临时节点, 是否是顺序节点
        self._zk_client.create("/rpc/server", addr1.encode(), ephemeral=True, sequence=True)
        self._zk_client.create("/rpc/server", addr2.encode(), ephemeral=True, sequence=True)

    def get_children(self, path):

        return self._zk_client.get_children(path)
