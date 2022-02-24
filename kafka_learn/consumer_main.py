# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

from kafka_learn.kafka_consumer import SelfKafkaConsumer
from kafka_learn.kafka_manager import topic


if __name__ == '__main__':
    consumer = SelfKafkaConsumer(topic)
    consumer.get_message()
