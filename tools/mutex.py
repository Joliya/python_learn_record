"""
@file: mutex.py
@time: 2023/11/20 18:04
@desc:
利用redis的原子操作，模拟进程间互斥锁
fake_mutex.__doc__ 及 fake_mutex_decorator.__doc__

fake_mutex：提供互斥操作
fake_mutex_decorator：互斥的装饰器
"""

import os
import threading
import time
from functools import wraps
from inspect import signature
from typing import TypeVar, Callable, Any

from tools.encoding import sha1_hex
from tools.sign_tools import sign_value

TF = TypeVar("TF", bound=Callable[..., Any])

__all__ = [
    "fake_mutex",
    "fake_mutex_decorator",
    "execute_once_during_decorator",
    "get_func_sign_call_args",
]


_thread_local = threading.local()


def _get_value() -> str:
    """
    获取应该存在redis中的数值，线程唯一
    :return: string
    """
    value = getattr(_thread_local, "mutex_value", None)
    if value:
        return value

    value = "%s_%s" % (os.getpid(), threading.currentThread().ident)
    _thread_local.mutex_value = value
    return value


class _RedisLockBase:
    def __init__(self, redis_cli: redis_client, mutex_name: str, lock_seconds: float,
                 blocking_seconds: float = -1, sleep_seconds: float = 0.01, allow_more: bool = True):
        """
        创建一个分布式锁
        :param redis_cli: Redis实例
        :param mutex_name: str, 锁名称，相同名称的锁一次只有一个实例能够获取
        :param lock_seconds: float/int, 独占锁时间
        :param blocking_seconds: float/int, 暂时无法获取锁时，最长等待时间(由于sleep误差，实际可能偏大)，如果小于等于0，直接返回
        :param sleep_seconds: float/int, 无法获取锁时尝试时间间隔
        """
        assert lock_seconds > 0, u'必须指定过期时间'
        self.redis = redis_cli
        self.mutex_name = "redis_lock_%s_180213" % mutex_name
        self.lock_seconds = lock_seconds
        self.blocking_seconds = blocking_seconds
        self.sleep_seconds = sleep_seconds
        self.token = _get_value()
        self.allow_more = allow_more

        if self.blocking_seconds > 0:
            assert 0 < self.sleep_seconds <= self.blocking_seconds, u"阻塞模式需要正确设置尝试间隔时间"

    def _check_token(self):
        if self.token != _get_value():
            self.token = _get_value()

    def do_acquire(self) -> bool:
        """
        尝试获取锁
        :return: bool，是否获取成功
        """
        raise NotImplementedError

    def acquire(self) -> bool:
        """
        获取锁资源
        :return: bool，是否成功获取锁
        """
        self._check_token()
        if self.blocking_seconds <= 0:
            try_count = 1
        else:
            try_count = int(self.blocking_seconds // self.sleep_seconds) + 1

        while True:
            try_count -= 1
            if self.do_acquire():
                return True
            if try_count <= 0:
                break
            time.sleep(self.sleep_seconds)
        return False

    def do_release(self) -> bool:
        """
        尝试释放锁资源
        :return: bool是否释放成功
        """
        raise NotImplementedError

    def release(self) -> bool:
        """
        释放锁资源
        :return: bool是否释放成功
        """
        self._check_token()
        return self.do_release()


class StrictRedisLock(_RedisLockBase):
    """
    利用Redis实现的分布式锁
    """
    ACQUIRE_CODE = {
        "lock": 1,
        "second_lock": 2,
        "fail": 0,
    }

    LUA_ACQUIRE_SCRIPT = """
    if redis.call('setnx', KEYS[1], ARGV[1]) == 1 then
        if ARGV[2] ~= '' then
            redis.call('pexpire', KEYS[1], ARGV[2])
        end
        return {lock}
    -- 允许同一个线程多次加锁，第二次加锁不会更新锁时间！！！
    elseif redis.call('get', KEYS[1]) == ARGV[1] then
        return {second_lock}
    else
        -- 防止由于异常导致expire设置失败情况(如, Ctrl+C等)
        if redis.call('ttl', KEYS[1]) == -1 then
            redis.call('pexpire', KEYS[1], ARGV[2])
        end
        return {fail}
    end
    """.format(**ACQUIRE_CODE)

    LUA_RELEASE_SCRIPT = """
        local token = redis.call('get', KEYS[1])
        if not token or token ~= ARGV[1] then
            return 0
        end
        redis.call('del', KEYS[1])
        return 1
    """

    def __init__(self, redis_cli, mutex_name, lock_seconds,
                 blocking_seconds=-1, sleep_seconds=0.01, allow_more=True):
        """
        创建一个分布式锁
        :param redis_cli: StrictRedis实例
        :param mutex_name: str, 锁名称，相同名称的锁一次只有一个实例能够获取
        :param lock_seconds: float/int, 独占锁时间
        :param blocking_seconds: float/int, 暂时无法获取锁时，最长等待时间(由于sleep误差，实际可能偏大)，如果小于等于0，直接返回
        :param sleep_seconds: float/int, 无法获取锁时尝试时间间隔
        """
        super(StrictRedisLock, self).__init__(redis_cli, mutex_name, lock_seconds, blocking_seconds, sleep_seconds,
                                              allow_more)

        self.lua_acquire = self.redis.register_script(self.LUA_ACQUIRE_SCRIPT)
        self.lua_release = self.redis.register_script(self.LUA_RELEASE_SCRIPT)

        self.need_release = False

    def do_acquire(self) -> bool:
        timeout = int(self.lock_seconds * 1000)
        from redis import RedisError
        try:
            result = self.lua_acquire(keys=[self.mutex_name], args=[self.token, timeout], client=self.redis)
        except RedisError:
            self.need_release = False
            # redis服务出现异常，允许获得锁资源
            return True

        # 只有在第一次获取锁的时候需要释放锁资源
        self.need_release = result == self.ACQUIRE_CODE["lock"]
        success_status = [self.ACQUIRE_CODE["lock"]]
        if self.allow_more:
            success_status.append(self.ACQUIRE_CODE["second_lock"])
        return result in success_status

    def do_release(self) -> bool:
        """
        释放锁资源
        :return: bool，是否释放成功
        """
        if not self.need_release:
            return False

        from redis import RedisError
        try:
            result = self.lua_release(keys=[self.mutex_name], args=[self.token], client=self.redis)
        except RedisError:
            return False

        return bool(result)


def fake_mutex(mutex_name, error_return=None, seconds=1, release_when_exit=True,
               blocking_seconds=-1, sleep_seconds=0.01, global_name=False, allow_more=True,
               redis_cli=redis_client):
    """
    可以直接作为decorator使用，这时整个函数都将互斥。
    如果需要按照部分参数互斥，则需要手动按参数构建mutex_name。
    允许同一个线程对同一个资源(函数)多次加锁
    e.g.
      假如有一个函数
        def need_mutex_func(user_id, *args, **kwargs): pass
      需要按用户互斥，调用者需要将代码
        need_mutex_func(user_id, *args, **kwargs)
      改成
        mutex_name = build_mutex_name(user_id)  # build函数用户自定义
        new_func = fake_mutex(mutex_name, error_return)(need_mutex_func)
        new_func(user_id, *args, **kwargs)

    note1
    按照现在使用习惯，希望有
      @fake_mutex('same_name')
      def foo(): pass

      @fake_mutex('same_name')
      def bar(): pass
    两个函数，foo, bar不互相影响，即foo, bar不互斥。如果希望其互斥，则可以
      @redis_mutex('same_name', global_name=True)
      def foo(): pass

      @fake_mutex('same_name', global_name=True):
      def bar(): pass
    这样, foo, bar的执行也会互斥。

    note2
    正常来说，一个获取了锁资源的函数执行完后，会立刻释放锁资源(release_when_exit=True)。
    有时，可能有的需求是一段时间内某个函数只会被执行一次，这个时候将release_when_exit设为False。

    :param mutex_name: 锁名称
    :param error_return: 获取锁失败时，返回值
    :param seconds: float/int, 独占锁时间，为了保证函数的互斥，需要比函数执行时间长
    :param release_when_exit: 参数上面注释 note2
    :param blocking_seconds: 如果大于0，在暂时获取不到锁资源的情况下，最多等待时间
    :param sleep_seconds: 等待期间尝试时间间隔
    :param global_name: 参考上面注释 note1
    :param allow_more: 允许一个线程多次加锁
    :param redis_cli:
    :return:
    """

    def _wrapper(func: TF) -> TF:
        lock_name = "%s" % mutex_name
        if not global_name:
            lock_name = "%s_%s_%s" % (mutex_name, func.__module__, func.__name__)
        redis_lock = StrictRedisLock

        # 避免太长的lock name
        lock_name = sha1_hex(lock_name)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            if seconds <= 0:
                return func(*args, **kwargs)
            lock = redis_lock(redis_cli=redis_cli, mutex_name=lock_name, lock_seconds=seconds,
                              blocking_seconds=blocking_seconds, sleep_seconds=sleep_seconds,
                              allow_more=allow_more)
            if lock.acquire():
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    if release_when_exit:
                        lock.release()
            else:
                return error_return

        return _wrapped_func

    return _wrapper


def fake_mutex_decorator(error_return=None, seconds=1,
                         blocking_seconds=-1, sleep_seconds=0.01, redis_cli=redis_client, allow_more=True,
                         first_n=None):
    """
    @see redis_mutex
    如果一个函数在所有参数相同的情况下需要互斥，可以简单使用这个装饰器
    注：用这个装饰器，相关互斥锁会在函数执行完就释放。只是避免"同一时间"的并发
      如果想要实现一个函数在一段时间内只执行一次（如避免用户重复请求等），需要使用`execute_once_during_decorator`
    first_n: 只对前n个参数互斥
    e.g.
      @fake_mutex_decorator(error_return)
      def need_mutex_func(*args, **kwargs): pass

      对于使用了first_n的，如
      @fake_mutex_decorator(first_n=2)
      def foo(a, b, c, d): pass

      调用时，前first_n个参数，只能使用位置参数，即只能使用
      foo(1, 2, d=3, c=4)的形式
      而不能使用 foo(a=1, b=2, c=3, d=4)
    """

    def _wrapper(func: TF) -> TF:
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            mutex_name = get_func_sign_call_args(func, first_n, *args, **kwargs)
            release_when_exit = True
            return fake_mutex(
                mutex_name, error_return, seconds, release_when_exit, blocking_seconds,
                sleep_seconds, global_name=False, allow_more=allow_more, redis_cli=redis_client,
            )(func)(*args, **kwargs)

        return _wrapped_func

    return _wrapper


def execute_once_during_decorator(seconds=60, error_return=None, only_same_para=True,
                                  redis_cli=redis_client, first_n=None):
    """
    在给定时间内，某个函数只执行一次
    :param seconds:
    :param error_return:
    :param only_same_para: 为True，则只有参数相同的情况下一个函数只执行一次；为False时，整个函数在给定时间只允许执行一次
    :param redis_cli: 指定redis
    :param first_n: 只有在only_same_para为True的情况下有意义。

    e.g.
      @execute_once_during_decorator()
      def foo(a, b):
         return a + b

      那么第一次执行foo(1, 2)时，返回的结果为3，一分钟内，再次执行foo(1, 2)，返回的结果为None。一分钟内首次执行foo(2, 1)不受影响，得到结果3
      1分钟后，相关锁自动释放

      ---
      @execute_once_during_decorator(only_same_para=False)
      def bar(a, b):
         return a + b

      那么第一次执行bar(1, 2)得到结果3，一分钟执行bar(a, b)，对于任何a, b都只能得到None的结果

      ---
      @execute_once_during_decorator(first_n=1)
      def foobar(a, b):
        return a + b

      一分钟内依次执行以下操作，得到的结果分别为
      1. foobar(1, 2)  -> 3
      2. foobar(1, 3)  -> None  # 被1互斥
      3. foobar(2, 1)  -> 3
      4. foobar(2, 2)  -> None  # 被3互斥
      5. foobar(2, b=3)  -> None  # 被3互斥
      6. foobar(a=1, b=2)  -> 异常，不允许这么调用
    """

    def wrapper(func: TF) -> TF:
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            mutex_name = "once_during_180227_%s_%s" % (func.__module__, func.__name__)
            if only_same_para:
                mutex_name += get_func_sign_call_args(func, first_n, *args, **kwargs)
            return fake_mutex(
                mutex_name, error_return, seconds, release_when_exit=False, allow_more=False, redis_cli=redis_cli
            )(func)(*args, **kwargs)

        return wrapped_func

    return wrapper


def get_func_sign_call_args(origin_func, first_n, *args, **kwargs):
    """
    获取函数调用时传入的参数的签名值用于构建redis键 https://docs.python.org/zh-cn/3/library/inspect.html#inspect.Signature.bind
    :param origin_func:
    :param first_n: 只取前n个参数，int or None
    :param args:
    :param kwargs:
    :return: str
    """
    func_signature = signature(origin_func)
    bind = func_signature.bind(*args, **kwargs)
    bind.apply_defaults()
    call_args = [bind.arguments[param_name] for param_name in func_signature.parameters]
    return sign_value(call_args) if first_n is None else sign_value(call_args[:first_n])
