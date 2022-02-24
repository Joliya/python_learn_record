# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

from kafka_learn.kafka_manager import topic
from kafka_learn.kafka_producer import SelfKafkaProducer


if __name__ == '__main__':
    producer = SelfKafkaProducer()

    feature = producer.send_message(topic, {"a": 1, "b": 2}, "112311")
