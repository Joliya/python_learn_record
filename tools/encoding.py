"""
@file: encoding.py
@time: 2024/7/26 18:50
@desc:
"""
from hashlib import sha1

import six


def ensure_utf8(str1, errors='strict'):
    if not str1:
        return b''
    if isinstance(str1, six.text_type):
        return str1.encode('utf-8', errors)
    return str1


def sha1_hex(content):
    """
    返回url的utf8编码对应的hex digest
    """
    content = ensure_utf8(content)
    return sha1(content).hexdigest()


def ensure_unicode(str1, errors='strict'):
    if not str1:
        return u''
    if isinstance(str1, six.text_type):
        return str1
    else:
        return str1.decode('utf-8', errors)
