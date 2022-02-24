# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

import time
import traceback

import six
from kafka import KafkaProducer
import simplejson as json
from kafka.errors import kafka_errors


class SelfKafkaProducer:
    """
    封装kafka 生产者
    """

    def __init__(self):
        self._producer = KafkaProducer(
            bootstrap_servers=['192.168.102.177:9092'],
            key_serializer=lambda k: json.dumps(k).encode("utf-8"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"))

    def _send_message(self, topic, message, key, timeout=0.5):
        """发送消息"""
        try:
            future = self._producer.send(topic, message, key)
            self._producer.flush()
            record_meta_data = future.get(timeout=10)  # 监控是否发送成功
            print(record_meta_data)
        except kafka_errors:  # 发送失败抛出kafka_errors
            traceback.format_exc()

    def send_message(self, topic, message, key):
        message = self.rebuild_message(message)
        self._send_message(topic, message, key)

    def rebuild_message(self, message):
        """
        如果是json字典（或者json.dumps后的字典）添加时间戳
        同时保证返回的结果类型是 bytes或者None
        正常来说，message只能是字符串，字典，None。
        :rtype: six.binary_type|types.NoneType
        """
        if message is None:
            return None

        if isinstance(message, dict):
            return self._rebuild_dict_message(message)

        if isinstance(message, bytearray):
            message = six.binary_type(message)
        elif isinstance(message, memoryview):
            message = message.tobytes()

        if not isinstance(message, (six.text_type, six.binary_type)):
            # 不认识的数据类型
            raise TypeError("unsupported type: {0}".format(type(message)))

        # message为字符串类型
        try:
            dict_message = json.loads(message)
            assert isinstance(dict_message, dict)
        except (json.errors.JSONDecodeError, AssertionError):
            return six.ensure_binary(message)

        return self._rebuild_dict_message(dict_message)

    def _rebuild_dict_message(self, message):
        """
        :rtype: six.binary_type
        """
        message['_ts_ms'] = int(time.time() * 1000)
        message_str = json.dumps(message)
        return six.ensure_binary(message_str)
