"""
@file: redis_container.py
@time: 2023/11/8 12:48
@desc:
"""
import time

"""
@file: redis_client.py
@time: 2023/10/31 14:41
@desc:
"""

import pickle

DAY_SECONDS = 60 * 60 * 24  # 一天对应的秒数
MONTH_SECONDS = 30 * 24 * 60 * 60


class _RedisStorageBase(object):
    """
    所有redis容器基类
    """

    def __init__(
            self,
            cache_key,
            redis_instance=redis_client,
            expire_time=DAY_SECONDS,
            need_decode=True,
    ):
        self._cache_key = cache_key
        self._redis_instance = redis_instance
        self._expire_time = expire_time
        self._need_decode = need_decode

    def clear(self):
        """
        删除所有元素
        """
        self._redis_instance.delete(self._cache_key)

    def cache_exists(self):
        """
        判断缓存是否存在
        :return: bool
        """
        return self._redis_instance.exists(self._cache_key)

    def _serialize(self, value):
        return value

    def _deserialize(self, value):
        return value

    def _expire(self):
        self._redis_instance.expire(self._cache_key, self._expire_time)


class RedisDict(_RedisStorageBase):
    """
    dict like redis storage
    使用 redis hset
    """

    def copy(self):
        """
        返回一个字典
        :return: dict
        """
        cached_dict = self._redis_instance.hgetall(self._cache_key)
        cached_dict = {key: self._deserialize(value) for key, value in list(cached_dict.items())}
        return cached_dict

    def get(self, key, default=None):
        """
        获取元素
        """
        value = self._redis_instance.hget(self._cache_key, key)
        if value is None:
            return default
        return self._deserialize(value)

    def mget(self, keys):
        """
        批量获取元素
        :param keys: list / tuple
        :return: {key: value}
        """
        if not keys:
            return {}
        value_list = self._redis_instance.hmget(self._cache_key, keys)
        result = {key: self._deserialize(value) for key, value in zip(keys, value_list)
                  if value is not None}
        return result

    def hincrby(self, key, amount=1):
        """
        整数元素自增
        """
        # 字典元素数据不能进行压缩或pickle
        return self._redis_instance.hincrby(self._cache_key, key, amount)

    def has_key(self, key):
        """
        判断是否存在键值为k的元素
        :param key:
        :return: bool
        """
        return self.__contains__(key)

    def items(self):
        """
        :return: list of (key, value)
        """
        copy_dict = self.copy()
        return list(copy_dict.items())

    def iteritems(self):
        """
        返回(key, value)的迭代器
        """
        return self._Iter(self)

    def keys(self):
        """
        :return: list of keys
        """
        return [key for key in self._redis_instance.hkeys(self._cache_key)]

    def values(self):
        """
        :return: list of values
        """
        value_list = self._redis_instance.hvals(self._cache_key)
        value_list = [self._deserialize(value) for value in value_list]
        return value_list

    def pop(self, key, default=None):
        """
        删除k, 并返回对应的value。如果没有对应的k, 返回d。
        和dict不同的是,这个地方不会抛KeyError异常
        :return: value
        """
        value = self.get(key, default)
        self._redis_instance.hdel(self._cache_key, key)
        return value

    def setdefault(self, key, value=None):
        """
        如果k不存在设置k对应的value为d
        :return: k对应的value值
        """
        save_value = self._serialize(value)
        is_set = self._redis_instance.hsetnx(self._cache_key, key, save_value)
        if is_set:
            self._expire()
            return value
        return self.get(key, value)

    def update(self, E=None, **F):
        """
        D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E present and has a .keys() method, does:     for k in E: D[k] = E[k]
        If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v
        In either case, this is followed by: for k in F: D[k] = F[k]
        """
        if not E:
            key_value_list = []
        elif hasattr(E, "keys"):
            key_value_list = [(k, E[k]) for k in E]
        else:
            key_value_list = [(k, v) for (k, v) in E]

        for k in F:
            key_value_list.append((k, F[k]))

        # 由于redis的pipeline没有实现hset_pickle, 这个地方先手动pickle
        key_value_list = [(k, self._serialize(v)) for (k, v) in key_value_list]

        pipeline = self._redis_instance.pipeline(transaction=False)
        for (key, value) in key_value_list:
            pipeline.hset(self._cache_key, key, value)
        pipeline.execute()

        if key_value_list:
            self._expire()

    def __contains__(self, item):
        """
        D.__contains__(y) --> True if D has a key k, else False
        """
        return self._redis_instance.hexists(self._cache_key, item)

    def __setitem__(self, key, value):
        """
        x.__setitem__(key, value) <==> x[key] = value
        """
        save_value = self._serialize(value)
        self._redis_instance.hset(self._cache_key, key, save_value)
        self._expire()

    def __delitem__(self, key):
        """
        x.__delitem__(key) <==> del x[key]
        """
        exists = self._redis_instance.hdel(self._cache_key, key)
        if exists == 0:
            raise KeyError(key)

    def __getitem__(self, key):
        """
        x.__getitem__(key) <==> x[key]
        与dict不同的是, 如果key不存在会返回None, 而不是抛KeyError异常
        """
        return self.get(key)

    def __iter__(self):
        """
        x.__iter__() <==> iter(x)
        如果有大量元素, 请使用iteritems()
        """
        key_list = list(self.keys())
        return iter(key_list)

    def __len__(self):
        """
        x.__len__() <==> len(x)
        """
        return self._redis_instance.hlen(self._cache_key)

    # =========== 其它方法, 兼容老版本 ============
    def set_value(self, key, value):
        self[key] = value

    def get_value(self, key):
        return self[key]

    def exists(self, key):
        return key in self

    def delete_keys(self, *keys):
        """
        删除一些key值
        :return: 被删除key的个数
        """
        if not keys:
            return 0
        return self._redis_instance.hdel(self._cache_key, *keys)

    # =========== 私有 ============
    class _Iter(object):
        """
        iteritems迭代器
        """

        def __init__(self, redis_dict, fetch_per_count=100):
            self.__redis_dict = redis_dict
            self.__redis_instance = redis_dict._redis_instance
            self.__cache_key = redis_dict._cache_key
            self.__deserialize = redis_dict._deserialize

            self.fetch_per_count = fetch_per_count
            self.__next_cursor = None
            self.__cur_values = None

        def __iter__(self):
            return self

        def __next__(self):
            if self.__next_cursor == 0 and not self.__cur_values:
                raise StopIteration

            if self.__cur_values:  # should be a dict
                key, value = self.__cur_values.popitem()
                value = self.__deserialize(value)
                return key, value

            cursor = self.__next_cursor if self.__next_cursor is not None else 0
            self.__next_cursor, self.__cur_values = \
                self.__redis_instance.hscan(self.__cache_key, cursor=cursor, count=self.fetch_per_count)
            return next(self)


class RedisSortedSet(_RedisStorageBase):
    """
    存储带有score的有序集合
    利用 redis zset
    """

    def add(self, value, score=None):
        """
        添加一个value
        :param value:
        :param score: 如果不给, 默认为当前时间戳
        """
        score = score if score is not None else time.time()
        self._redis_instance.zadd(self._cache_key, {self._serialize(value): score})
        self._expire()

    def madd(self, score_map):
        """
        添加元素, 需要注意的是, 这个方法与add方法score和value顺序不一致!
        :param score_map: {name1: score1, name2: score2}
        :return:
        """
        args = {}
        for key in list(score_map.keys()):
            args[self._serialize(key)] = score_map[key]
        if not args:
            return
        self._redis_instance.zadd(self._cache_key, args)
        self._expire()

    def remove(self, *values):
        """
        移除values
        :return: 被移除元素个数
        """
        if not values:
            return 0
        value_list = [self._serialize(v) for v in values]
        return self._redis_instance.zrem(self._cache_key, *value_list)

    def values_by_score(self, min_score="-inf", max_score="+inf", start=None, num=None, reverse=False):
        """
        获取指定score区间内的元素
        :return: [value], list of value
        """
        if not reverse:
            value_list = self._redis_instance.zrangebyscore(self._cache_key, min_score, max_score, start, num)
        else:
            value_list = self._redis_instance.zrevrangebyscore(self._cache_key, max_score, min_score, start, num)

        return [self._deserialize(value) for value in value_list]

    def values_by_score_with_score(self, min_score="-inf", max_score="+inf", start=None, num=None, reverse=False):
        """
        获取指定score区间内的元素, 并返回对应的score值
        :return: [(value, score)], list of (value, score)
        """
        if not reverse:
            value_list = self._redis_instance.zrangebyscore(self._cache_key, min_score, max_score,
                                                            start, num, withscores=True)
        else:
            value_list = self._redis_instance.zrevrangebyscore(self._cache_key, max_score, min_score,
                                                               start, num, withscores=True)

        return [(self._deserialize(value), score) for (value, score) in value_list]

    def values_by_range(self, start=0, end=-1, reverse=False):
        """
        返回指定区间内的元素
        :return: [value], list of value
        """
        if reverse:
            value_list = self._redis_instance.zrevrange(self._cache_key, start, end)
        else:
            value_list = self._redis_instance.zrange(self._cache_key, start, end)
        return [self._deserialize(value) for value in value_list]

    def values_by_range_with_score(self, start=0, end=-1):
        """
        返回指定区间内的元素
        :return: [(value, score)], list of (value, score)
        """
        value_list = self._redis_instance.zrange(self._cache_key, start, end, withscores=True)
        return [(self._deserialize(value), score) for (value, score) in value_list]

    def count_within_score(self, min_score="-inf", max_score="+inf"):
        """
        获取score介于给定score之间的元素个数
        注: 如果获取所有元素数量，请使用 len, @see __len__
        :return: int
        """
        return self._redis_instance.zcount(self._cache_key, min_score, max_score)

    def update_score(self, score, value, set_flag=False):
        """
        更新value对应的score值, 如果value不存在会加入value
        :param value:
        :param score:
        :param set_flag: 如果为True, 将分值设为score, 否则在原来基础上增加score
        :return: 新的score值
        """
        if set_flag:  # 这种情况, 直接调用插入方法更新score值
            self.add(value, score)
            return score

        save_value = self._serialize(value)
        now_score = self._redis_instance.zincrby(self._cache_key, score, save_value)
        self._expire()
        return now_score

    def score(self, value):
        """
        获取value对应的score值
        :param value:
        :return: float, 如果value存在, 否则返回None
        """
        save_value = self._serialize(value)
        return self._redis_instance.zscore(self._cache_key, save_value)

    def remove_range_by_score(self, min_score, max_score):
        """
        删除score值介于min_score和max_score之间(包括边界)的成员
        :param min_score:
        :param max_score:
        :return: 被移除成员的数量
        """
        return self._redis_instance.zremrangebyscore(self._cache_key, min_score, max_score)

    def remove_range_by_rank(self, start, stop):
        """
        删除位于排名内的成员，包含start, stop
        :param start: 以0为底, -1表示最后一个成员
        :param stop:
        :return: 被移除成员的数量
        """
        return self._redis_instance.zremrangebyrank(self._cache_key, start, stop)

    def __len__(self):
        """
        x.__len__() <==> len(x)
        """
        return self._redis_instance.zcard(self._cache_key)

    def __contains__(self, value):
        save_value = self._serialize(value)
        score = self._redis_instance.zscore(self._cache_key, save_value)
        return score is not None

    def __iter__(self):
        """
        x.__iter__() <==> iter(x)
        迭代返回(name, value)值
        """
        return self._Iter(self)

    # =========== 私有 ============
    class _Iter(object):
        def __init__(self, redis_set, fetch_per_count=100):
            self.__redis_set = redis_set
            self.__redis_instance = redis_set._redis_instance
            self.__cache_key = redis_set._cache_key
            self.__deserialize = redis_set._deserialize

            self.fetch_per_count = fetch_per_count
            self.__next_cursor = None
            self.__cur_values = None

        def __iter__(self):
            return self

        def __next__(self):
            if self.__next_cursor == 0 and not self.__cur_values:
                raise StopIteration

            if self.__cur_values:  # should be list
                value, score = self.__cur_values.pop()
                return self.__deserialize(value), score

            cursor = self.__next_cursor if self.__next_cursor is not None else 0
            self.__next_cursor, self.__cur_values = \
                self.__redis_instance.zscan(self.__cache_key, cursor=cursor, count=self.fetch_per_count)

            return next(self)
