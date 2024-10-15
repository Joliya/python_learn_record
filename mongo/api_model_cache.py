# -*- coding:utf-8 -*-
"""
model级的数据库缓存
使用方法如下：
add_flask_cache_manager

class ModelA(models.Model):

    col_1 = models.CharField(max_length=100, unique=True)
    col_2 = models.IntegerField(choices=WEEK_DAY_CHOICES)

# 根据ID获取时可用  ModelA.cache.get(id=xxx)
add_flask_cache_manager(ModelA, model_redis)

# 根据col_1获取时可用  ModelA.cache.get(col_1=xxx)
add_flask_cache_manager(ModelA, model_redis, unique_keys=(('col_1', )))

# 多种方式联合 ModelA.cache.get(id=xxx)  ModelA.cache.get(col_1=xxx)
add_flask_cache_manager(ModelA, model_redis, unique_keys=(('id'), ('col_1')))
"""
from __future__ import absolute_import
from __future__ import print_function

import pickle
import zlib

import six
from mongoengine import pre_save, post_delete, post_save, StringField
from mongoengine.base import BaseDocument

from tools.encoding import sha1_hex, ensure_unicode

DEFAULT_KEY = "defaults"

# 单位: 秒(s)【因为model cache在save时会更新过期时间；且根据热点数据规律，一般保存2天就足够满足需求】
DEFAULT_MODEL_CACHE_TIME = 60 * 60 * 24 * 2
# DEFAULT_MODEL_CACHE_TIME = 60 * 1

PICKLE_PROTOCOL = 4


def build_post_dispatch_uid(model_class, category):
    uid = model_class.__module__ + '#' + model_class.__name__ + ('_%s_identifier' % category)
    return sha1_hex(uid)


def _get_unique_keys(sender, instance):
    """
    获取instance对应的unique key的相对应的key, 例如:
    id -->  table_prex:id:10000:version --> sha1 digest
    :param sender:
    :param instance:
    :return:
    """
    cache_manager = sender.cache
    result = []
    unique_key_set = cache_manager.unique_key_set
    for unique_key in unique_key_set:
        key = cache_manager._build_model_key_for_attrs(unique_key, instance)
        result.append(key)
    return result


def _try_get_old_instance(instance):
    """
    尝试从数据库重新获取instance对象
    :param instance:
    :return:
    """
    try:
        model_cls = instance.__class__
        pk_attname = model_cls._meta["id_field"]
        query_dict = {pk_attname: instance.pk}
        return model_cls.cache.get(**query_dict)
    except BaseException:
        return None


def delete_model_cache_by_instance_for_pre_save(instance, document, **kwargs):
    """
    pre_save自动调用，删除老的实例对应的cache
        1. 如果cache_key变化了，需要删除，否则通过老的cache_key还能获取到旧数据，比如model.cellphone变了，cellphone是cache_key
        2. db保存成功, post_save fail，这时候不管cache_key是否变化，也需要清理老的cache
    :param document: document instance
    :param instance: model instance
    :param kwargs:
    """
    # 判断有没有cache，
    if not document or not isinstance(getattr(document, "cache", None), FlaskCacheManager):
        return
    # 首次创建肯定没有缓存，不需要下面_try_get_old_instance这种必然db不命中的操作
    if not getattr(document, 'pk', None):
        return
    model_cls = document.__class__
    unique_key_list = model_cls.cache.unique_key_list
    # 如果只有主键作为cache_key，那么不需要多一次额外的获取old_instance的操作
    if len(unique_key_list) == 1 and unique_key_list[0][0] == model_cls._meta["id_field"]:
        attr_list_keys = _get_unique_keys(model_cls, document)
    else:
        old_instance = _try_get_old_instance(document)
        attr_list_keys = _get_unique_keys(model_cls, old_instance) if old_instance else []
    _delete_model_cache(model_cls, attr_list_keys)


def delete_model_cache_by_instance_for_post_delete(instance, document, **kwargs):
    """
    post_delete自动调用，删除当前实例对应的cache，保证删除后不能通过cache获取到
    :param document:
    :param instance: model instance
    :param kwargs:
    """
    # 判断有没有cache，
    if not document or not isinstance(getattr(document, "cache", None), FlaskCacheManager):
        return
    model_cls = document.__class__
    attr_list_keys = _get_unique_keys(model_cls, document)
    _delete_model_cache(model_cls, attr_list_keys)


def _delete_model_cache(model_cls, attr_list_keys):
    if not attr_list_keys:
        return
    cache = model_cls.cache
    try:
        cache.redis_client.delete(*attr_list_keys)
    except Exception:
        for key in attr_list_keys:
            cache.redis_client.delete(key)


def update_model_cache_by_instance(instance, document, **kwargs):
    """
    一般由post_save调用
    :param document:
    :param instance: model instance
    :param kwargs:
    :return:
    """
    if not document or not isinstance(getattr(document, "cache", None), FlaskCacheManager):
        return
    save_model_to_cache(document)


def save_model_to_cache(instance, key_list=None, only_not_exist=False):
    """
    保存model对象instance到缓存中
    :param instance:
    :param key_list:
    :param only_not_exist:
    :return:
    """
    model_cls = instance.__class__
    cache = model_cls.cache
    redis_client = cache.redis_client
    expire_time = cache.model_expiration
    if key_list is None:
        key_list = _get_unique_keys(model_cls, instance)
    value = model_2_data_new(instance)
    for key in key_list:
        redis_client.set(key, value, ex=expire_time, nx=only_not_exist)


def _is_version_valid(version):
    if version is None:
        return True
    if isinstance(version, six.integer_types):
        return True
    if isinstance(version, six.string_types):
        return True
    return False


class FlaskCacheManager(object):
    """
    1. 根据使用频率: 大部分对象的访问都是通过id进行读写的，主要是作为ForeignKey来进行读写
    2. 存在部分情况，需要通过其他的Key来读取数据, 例如: username ---> user
       但是这种情况的概率不高，只有在登陆的时刻才需要，因此不做cache

    3. 提供有限的几种查询方式
       User.cache.get()
                 .get_or_create()
                 .delete()

       全功能的操作请继续使用默认的方式: User.objects.xxx

       cache是一个通用的设计，不可能实现所有的.objects的功能，因为.objects存在多种实现

    注：有些场景可能希望知道缓存时使用的key值，以及是否命中缓存等信息，
    可以手动先调用 User.cache._debug = True，会额外print一些信息
    """

    def __init__(self, model_class, unique_keys=(('_id',),), redis_client=None, model_expiration=None, version=None):
        if not model_class:
            return

        assert isinstance(unique_keys, (list, tuple)) and len(unique_keys) > 0 and isinstance(unique_keys[0],
                                                                                              (list, tuple))

        self.model_class = model_class
        model_meta = get_model_meta(model_class)
        self.model_version = model_meta.version
        self.name2attname = model_meta.name2attname
        self.model_expiration = model_expiration or DEFAULT_MODEL_CACHE_TIME  # 支持传递过期时间
        self.redis_client = redis_client
        assert _is_version_valid(version), u"version只允许为字符串或者整数"
        version = "%s_%s" % (version or "", model_meta.version)  # 保证model改变后，丢弃老数据
        self.cache_version = version

        self._debug = False

        # 记录不同字段组合对应的索引键需要的字段名
        self.unique_key_set = set([tuple(sorted(key)) for key in unique_keys])
        self.unique_key_list = list(self.unique_key_set)

        # 函数内定义的局部函数注册post_save后并不生效，所以挪到外部
        # pre_save在更新前删除数据主要是对于修改了unique_keys本身的情况下，通过老数据不应该能继续获取到数据。如：
        # >>> old_name = user.username
        # >>> user.username = new_name
        # >>> user.save()
        # >>> User.cache.get(username=old_name) 期望获取不到数据
        # 但是这样一个进程写数据，一个进程读数据可能会导致cache, db不一致的问题，解决方案@see _get方法下面注释
        pre_save.connect(delete_model_cache_by_instance_for_pre_save, sender=model_class)
        post_delete.connect(delete_model_cache_by_instance_for_post_delete, sender=model_class)
        # buggy: 并发写时，可能会导致数据库，缓存数据不一致
        post_save.connect(update_model_cache_by_instance, sender=model_class)

    def get_model(self, key, model_class):
        """
        从 model_redis中读取 指定key对应的model_class对象
        :param key:
        :param model_class:
        :return:
        """
        data = self.redis_client.get(key)
        if not data:
            return None
        else:
            return data_2_model_new(data, self.model_class)

    def get(self, **kwargs):
        """
            通过id, 或unique_key来读取数据, 大部分情况都是通过id, unique_key来读取数据的
            :param kwargs:
            :return:
        """
        val, __ = self._get(**kwargs)
        return val

    def get_or_404(self, **kwargs):
        try:
            val, __ = self._get(**kwargs)
            return val
        except:
            return None

    def invalidate(self, **kwargs):
        return self.invalidate_cache(**kwargs)

    def invalidate_cache(self, **kwargs):
        """
            注意: 注意数据的一致性
        """
        keys = tuple(sorted(kwargs.keys()))
        if self._is_cache_valid_attr(keys):
            key = self._build_model_key_for_attrs(keys, kwargs)
            return self._invalidate_model(key)
        else:
            assert False

    def delete_cache(self, **kwargs):
        """
            删除attr_list的cache
        """
        keys = tuple(sorted(kwargs.keys()))

        if self._is_cache_valid_attr(keys):
            key = self._build_model_key_for_attrs(keys, kwargs)
            self.redis_client.delete(key)
        else:
            assert False

    def _is_cache_valid_attr(self, sorted_keys_tuple):
        """
            直接通过set快速操作
            :param sorted_keys_tuple:
            :param keys_set:
            :return:
        """
        return sorted_keys_tuple in self.unique_key_set

    def _get(self, **kwargs):
        """
            如果is_get_or_create=False, 返回value, False
            如果is_get_or_create=True, 返回value, created(是否新创建)
        """
        sorted_keys = tuple(sorted(kwargs.keys()))

        key = None
        if self._is_cache_valid_attr(sorted_keys):
            key = self._build_model_key_for_attrs(sorted_keys, kwargs)
            if self._debug:
                print('key -->', key)

            # 从Cache中读取到了数据
            val = self.get_model(key, self.model_class)

            if val:
                if self._debug:
                    print('cache hit')
                val._id = val.pk
                return val, False

        # 直接从数据库读取数据
        val = self.model_class.objects.get(**kwargs)
        ret_val = val, False

        # 更新Cache，加个判断cache里面有没有防止出现情况：
        # 1. 数据库内数据为old, cache中没有数据
        # 2. 进程1获取数据，由于cache中没有，从数据库读的数据old
        # 3. 进程2将数据库数据, cache都更新为new
        # 4. 进程1获取过程继续执行，将cache写成old，从而导致数据库、cache不一致
        if key:
            save_model_to_cache(val, [key], only_not_exist=True)
        return ret_val

    def _build_model_key_for_attrs(self, sorted_keys, attr_dict_or_model):
        """
        model的key的计算: 假定attr_dict是有效的?
        """
        is_model = isinstance(attr_dict_or_model, BaseDocument)
        # 保证有序
        values = []
        for key in sorted_keys:
            # id --> id
            # user --> user_id
            key1 = self.name2attname.get(key, key)
            values.append(key1)

            # 如何处理value呢?
            # name = "hello" --> "hello"
            # user_id = 10   --> 10
            # user = User    --> user.id
            # user = 10      --> 10
            if is_model:
                # 尽量读取 user_id, 避免读取user, 否则可能导致多余的数据库/Redis请求
                value = getattr(attr_dict_or_model, key1)
            else:
                value = attr_dict_or_model.get(key)

            if value and isinstance(value, BaseDocument):
                value = value.pk

            values.append("%s" % value)

        attr_str = ":".join(values)
        table_key = ModelMeta.model_key(self.model_class)
        key = "%s#%s#%s#" % (table_key, attr_str, self.model_version)
        if self.cache_version is not None:
            key += '#%s' % self.cache_version
        return sha1_hex(key)

    def _invalidate_model(self, key):
        """
        删除key对应的cache, 如果成功删除返回True, 否则返回False
        :param key:
        :return:
        """
        return self.redis_client.delete(key) == 1


def add_cache_manager(model_class, redis_client, unique_keys=(('_id',),), expire_seconds=None, version=None):
    """
    为制定的Model添加基于redis_client的cache支持, 不同的Model可以选择不同的cache
    :param model_class: 数据库model名字
    :param redis_client: redis实例
    :param unique_keys: 需要查询的key列表
    :param expire_seconds: model过期时间，单位为秒(结合redis_client使用)
    :return:
    """
    # 如果传递expire_seconds值，确保为整数，保证调用正确
    if expire_seconds:
        assert isinstance(expire_seconds, int)
    model_class.cache = FlaskCacheManager(model_class, unique_keys, redis_client, expire_seconds, version)


def model_cache(model_cls=None, unique_keys=(('_id',),), expire_seconds=None, version=None, redis_client=None):
    """
    ModelCache 注册修饰器:

    @model_cache(unique_keys=[("user_id",), ])
    class MyUser(models.Model):
        pass

    或者：

    @model_cache
    class MyUser(models.Model):
        pass

    :param model_cls: 需要被修饰的类
    :param unique_keys: 需要查询的key列表，默认为 (('_id', ),)
    :param expire_seconds: model过期时间，单位为秒(结合redis_client使用)
    :param version: cache_version
    :param redis_client: redis实例，默认为 model_cache
    """

    def _model_wrapper(model_class):
        add_cache_manager(model_class, redis_client, unique_keys=unique_keys,
                          expire_seconds=expire_seconds, version=version)
        return model_class

    if model_cls:
        return _model_wrapper(model_cls)
    return _model_wrapper


class ModelMeta(object):
    def __init__(self, fields, name2attname, version):
        # 记录了Model中需要序列化的字段(Field), ModelClass._meta.local_fields
        self.fields = fields

        # 记录了 name 和 attname不一致的情况
        self.name2attname = name2attname

        # 记录了当前Model的version
        self.version = version

    @staticmethod
    def model_key(model_class):
        meta = model_class._meta
        model_name = meta.get("collection")
        return "%s.%s" % (model_class.__module__, model_name)


model_2_modelmeta = dict()


def get_model_meta(model_class):
    """
    获取Model的Meta信息
    """
    key = ModelMeta.model_key(model_class)

    if key not in model_2_modelmeta:
        # name, attname, column
        # 默认情况下，三个相同，但是对于外键元素，后两个相同
        # 也可以手动指定column, 使得attname和column不同
        #
        # 例如: Doctor
        #       user = ForeignKeyField(xxx)
        #     这里就只处理字段: user_id, 而不处理user, 防止外键引用被cache
        local_fields = []
        field_names = []
        for field_name, field in model_class._fields.items():
            local_fields.append(field)
            field_names.append(field_name)

        # 只保留不一样的地方
        name2attname = {}

        # Model的版本: 将Model所有的字段的名字相加，并且计算sha1 digest
        #
        # 不能排序: local_fields和代码定义相关，按照从上到下的顺序记录各个字段; 也和Model的初始化参数的顺序有关，如果代码字段做了调整，则cache失效
        fields = "".join(field_names)
        version = sha1_hex(fields)

        model_meta = ModelMeta(local_fields, name2attname, version)
        model_2_modelmeta[key] = model_meta
        return model_meta
    else:
        return model_2_modelmeta[key]


def fix_bytes_value(field, value):
    if isinstance(field, (StringField, )) and isinstance(value, six.binary_type):
        return ensure_unicode(value)
    return value


def ensure_pickle_loads(data, need_decode=True):
    """
    python3下，使用latin1 encoding多试一次
    https://docs.python.org/3/library/pickle.html#pickle.Unpickler
    Using encoding='latin1' is required for unpickling NumPy arrays and instances of datetime, date and time pickled by Python 2.
    :param data:
    :param need_decode: 字符串是否按转为unicode
    :return:
    """
    if six.PY2:
        return pickle.loads(data)
    else:
        first_encoding = "utf-8" if need_decode else "ASCII"
        second_encoding = "latin1" if need_decode else "bytes"
        try:
            return pickle.loads(data, encoding=first_encoding)
        except:
            result = pickle.loads(data, encoding=second_encoding)
            return recursive_convert_bytes_to_str(result) if need_decode else result


def recursive_convert_bytes_to_str(value):
    if value is None:
        return value
    elif isinstance(value, six.binary_type):
        return ensure_unicode(value)
    # 不需要处理的常见类型提前返回
    elif isinstance(value, six.text_type) or isinstance(value, six.integer_types) or isinstance(value, bool):
        return value
    elif isinstance(value, dict):
        return {recursive_convert_bytes_to_str(k): recursive_convert_bytes_to_str(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [recursive_convert_bytes_to_str(item) for item in value]
    elif isinstance(value, set):
        return {recursive_convert_bytes_to_str(item) for item in value}
    elif isinstance(value, tuple):
        return tuple([recursive_convert_bytes_to_str(item) for item in value])
    else:
        return value


def model_2_data_new(instance):
    """
    model对象序列化
    pickle + zlib
    :param instance:
    :return:
    """
    meta = get_model_meta(instance.__class__)
    # 保证写入的是正确的数据类型,有时候客户端会写入一些需要转型的数据，比如int传str，数据库没事，cache会出错
    # 这里强制field_to_python下
    values = [field.to_python(getattr(instance, field.name, None)) for field in meta.fields]
    pickle_data = pickle.dumps(values, protocol=PICKLE_PROTOCOL)
    compressed_data = zlib.compress(pickle_data)
    return compressed_data


def data_2_model_new(data, model_cls):
    """
    model对象反序列化
    pickle + zlib
    :param data:
    :param model_cls:
    :return:
    """
    decompressed_data = zlib.decompress(data)
    data_list = ensure_pickle_loads(decompressed_data)
    meta = get_model_meta(model_cls)
    value = {field.name: fix_bytes_value(field, val) for field, val in zip(meta.fields, data_list)}
    # 直接调用了构造函数， self._state 被正确设置
    return model_cls(**value)
