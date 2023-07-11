"""
令牌桶算法实现限流
"""
import datetime
import re
import time

radis = None # 假设这是redis 实例

rate_re = re.compile()

_periods = {
    "s": 1,
    "m": 60,
    "h": 24 * 60,
    "d": 24 * 60 * 60
}



def rate_limit(target_type="ip", rate="5/1m"):
    # 计算限制频率
    suffix = f"base,{target_type},{rate}"
    limit_key = f"_rate_limiter_{suffix}"





def split_rate(rate):
    """
    计算 频率， 主要是 计算出来 多少次， 以及 时间（秒）
    :param rate:
    :return:
    """
    count, multi, period = rate_re.match()
    count = int(count)
    seconds = _periods[period.lower()]
    return count, seconds


class RateLimiter:
    """
    限流器
    :param name:
    :param rate:
    :param redis_instance:
    :return:
    """

    MAX = 1000000

    def __init__(self, name, rate, redis_instance):
        self.name = name
        self.permits, self.seconds = split_rate(rate)
        self.micorseconds = int(self.seconds * self.MAX)
        self.micro_second_per_permit = int
        self.rate = rate
        self.redis_instance = redis_instance

    def build_key(self):
        return f"ratelimiter_{self.name}"

    def init_permits(self):
        now_time = datetime.datetime.now()  # 需要转， 这儿先不写了
        return self.redis_instance.set(self.build_key(), now_time - self.micorseconds)

    def acquire(self):
        redis_key = self.build_key()
        last_permit_time = int(self.redis_instance.get(redis_key) or 0)
        now_time = int(time.time() * self.MAX)
        delta_time = now_time - last_permit_time
        if delta_time > self.micorseconds:
            # 这块进行初始化， 如果使用在并发的情况下， 这儿加锁
            self.init_permits()
        elif delta_time < self.micorseconds:
            # 这儿就是令牌耗尽了
            return False

        # 刷新一下过期时间
        self.redis_instance.expire(redis_key, self.seconds)
        # 尝试获取令牌
        new_permit_time = int(self.redis_instance.incrby(redis_key, self.micro_second_per_permit))
        if new_permit_time > now_time:
            # 令牌被拿完了 ，回退一下
            self.redis_instance.incrby(redis_key, -self.micro_second_per_permit)
            return False
        return True



