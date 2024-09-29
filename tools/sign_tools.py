"""
@file: sign_tools.py
@time: 2023/11/20 18:15
@desc:
"""


import simplejson as json
import six


class ParaNotSupportError(Exception):
    """
    包含不能cache参数的错误
    """
    pass


class _StrJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, '_id'):
            return o.id
        try:
            from mongoengine import DynamicDocument
            # 如果是model，使用主键值
            if isinstance(o, DynamicDocument):
                return o.pk
        except ImportError:
            pass
        return six.text_type(o)


def sign_value(value):
    return json.dumps(value, cls=_StrJsonEncoder, sort_keys=True)


# ===================================================================
#                保证 _is_valid_cache_para 方法有效
# ===================================================================

def __guard():
    hex_id = hex(id(__guard))
    str_res = six.text_type(__guard)
    assert str_res[-len(hex_id) - 1:-1] == hex_id, u"_is_suitable_for_sign will not work now!!!"


__guard()
