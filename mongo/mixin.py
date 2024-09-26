"""
@file: mixin.py
@time: 2024/3/26 14:47
@desc:
"""
import simplejson as json


class ExtraInfoMixin(object):
    EXTRA_SORT_KEYS = False
    EXTRA_ENSURE_ASCII = False

    @property
    def _cached_extra_info_dict(self):
        """
        :rtype: dict
        """
        return json.loads(self.extra_info_str) if self.extra_info_str else {}

    @_cached_extra_info_dict.setter
    def _cached_extra_info_dict(self, extra_info_dict):
        self.extra_info_str = json.dumps(extra_info_dict, ensure_ascii=self.EXTRA_ENSURE_ASCII,
                                         sort_keys=self.EXTRA_SORT_KEYS)
        return extra_info_dict

    def get_extra_info_dict(self):
        """
        将extra_info json形式的字符串转换成一dict
        :return: dict
        """
        return self._cached_extra_info_dict

    def set_extra_info_dict(self, extra_info_dict):
        """
        设置extra_info的值。
        注意: 不会主动保存到数据库，如需更新到数据库，需额外调用save方法
        """
        self._cached_extra_info_dict = extra_info_dict

    def get_extra_info_with_key(self, key, default=None):
        """
        从extra_info中获取指定key的值，如果该key不存在返回default
        """
        return self._cached_extra_info_dict.get(key, default)

    def set_extra_info_with_key(self, key, value):
        """
        将extra_info中的指定key的值设为value(没有，添加)
        """
        extra_info_dict = self.get_extra_info_dict()
        extra_info_dict[key] = value
        self.set_extra_info_dict(extra_info_dict)

    def delete_extra_info_with_key(self, key):
        """
        删除某个key
        RET: 是否有修改
        """
        extra_info_dict = self.get_extra_info_dict()
        if key in extra_info_dict:
            extra_info_dict.pop(key)
            self.set_extra_info_dict(extra_info_dict)
            return True
        return False

    def update_extra_info_dict(self, update_dict):
        """
        将update_dict字典更新到extra_info
        """
        extra_info_dict = self.get_extra_info_dict()
        extra_info_dict.update(update_dict)
        self.set_extra_info_dict(extra_info_dict)

    # 为了兼容函数名差异
    def get_extra_info(self, key, default=None):
        return self.get_extra_info_with_key(key, default)

    def set_extra_info(self, key, value):
        """
        向extra_info里添加对应域
        """
        self.set_extra_info_with_key(key, value)

    def delete_extra_info(self, key):
        """
        向extra_info里删除对应域
        """
        return self.delete_extra_info_with_key(key)

    def update_extra_info(self, update_dict):
        self.update_extra_info_dict(update_dict)


NOT_EXIST_ID = 0


class QueryManagerMixin(object):
    """
    query manager mixin, 提供通用的查询函数

    使用方法：

    class MyModel(BaseDocument, QueryManagerMixin):
        pass

    ...

    def get_my_model_by_field_db_safe(field_value):
        return MyModel.get_by_field_safe(field=field_value)

    """

    @classmethod
    def get_by_id_safe(cls, instance_id):
        """
        按主键获取数据, 如果不存在返回None
        """
        if not instance_id or instance_id == "undefined":
            return None
        return cls.get_by_field_safe(_id=instance_id)

    @classmethod
    def get_by_field_safe(cls, *args, **kwargs):
        """
        按某个字段获取数据, 不存在返回None
        """
        try:
            if hasattr(cls, "cache"):
                return cls.cache.get(*args, **kwargs)
            else:
                return cls.objects.get(*args, **kwargs)
        except cls.DoesNotExist:
            return None
