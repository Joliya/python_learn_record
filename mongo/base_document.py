"""
@file: base_document.py
@time: 2024/3/26 14:23
@desc:
"""
import datetime
import json
import pickle

from mongoengine import DynamicDocument, StringField, DoesNotExist

from models.cache_document import CacheDynamicDocument
from models.mixin import ExtraInfoMixin, QueryManagerMixin
from tools.time_util import get_now_str, FORMAT_DATETIME, str_to_datetime, datetime_to_str


class BaseDocument(DynamicDocument, QueryManagerMixin):

    created_time = StringField(default="")
    last_modified = StringField(default="")

    meta = {'abstract': True}

    def save(self, **kwargs):
        now = get_now_str()
        if not self.created_time:
            self.created_time = now
        self.last_modified = now
        super().save(**kwargs)

    @classmethod
    def get_by_id(cls, _id):
        return cls.get_by_id_safe(_id)

    @classmethod
    def get_by_field(cls, *arg, **kwargs):
        return cls.get_by_field_safe(*arg, **kwargs)

    @property
    def to_dict(self):
        info = self.to_json()
        return json.loads(info)


class BaseCacheDocument(CacheDynamicDocument):

    created_time = StringField()
    last_modified = StringField()

    meta = {'abstract': True}

    def save(self, **kwargs):
        now = get_now_str()
        if not self.created_time:
            self.created_time = now
        self.last_modified = now
        super().save(**kwargs)

    @classmethod
    def get_by_field(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except DoesNotExist:
            return None


class ModelWithExtraInfo(DynamicDocument, ExtraInfoMixin):
    """
    抽象model，提供一json格式的字典的extra_info域。
    """

    meta = {'abstract': True}

    extra_info_str = StringField(help_text="json字典形式的额外信息")

    @staticmethod
    def simple_property(property_name, default, omit_none_value=False):
        pickled_default = pickle.dumps(default)  # 避免 [], {} 等可变类型被修改

        def get_property(self):
            return self.get_extra_info_with_key(property_name, pickle.loads(pickled_default))

        def set_property(self, value):
            if value is None and omit_none_value:
                self.delete_extra_info_with_key(property_name)
            else:
                self.set_extra_info_with_key(property_name, value)

        def del_property(self):
            self.delete_extra_info_with_key(property_name)

        return property(get_property, set_property, del_property)

    @staticmethod
    def datetime_property(property_name, default=None, format_str=FORMAT_DATETIME, omit_none_value=False):
        """
        :param property_name: datetime字段名称
        :param default: 默认值,只允许None和Dateteime类型
        :param format_str: 格式化规则 默认 FORMAT_DATETIME = %Y-%m-%d %H:%M:%S
        :param omit_none_value: 是否忽略空值
                                    为True时 赋值None表示删除key，再取会取出default
                                    为False时，赋值None会保存，再取会取出None
        """
        assert isinstance(default, datetime.datetime) or default is None

        def get_property(self):
            dt_str = self.get_extra_info_with_key(property_name)
            if dt_str is None:
                return default
            return str_to_datetime(dt_str, date_format=format_str, process_none=True)

        def set_property(self, value):
            assert isinstance(default, datetime.datetime) or default is None
            if value is None and omit_none_value:
                self.delete_extra_info_with_key(property_name)
            else:
                self.set_extra_info_with_key(property_name, datetime_to_str(value, format_str, process_none=True))

        def del_property(self):
            self.delete_extra_info_with_key(property_name)

        return property(get_property, set_property, del_property)
