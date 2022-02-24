# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

from kafka import KafkaConsumer
import json


class SelfKafkaConsumer:
    """
    封装kafka 生产者
    """

    def __init__(self, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=['192.168.102.177:9092', '192.168.102.177:9093'],
        )
        print(self.consumer.topics())

    def get_consumer(self):
        return self.consumer

    def get_message(self):
        print(self.consumer.config)
        for record in self.consumer:
            print(json.loads(record.value))
