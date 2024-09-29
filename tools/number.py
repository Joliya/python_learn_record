"""
@file: number.py
@time: 2023/11/23 11:14
@desc:
"""
import math
import random
import string


def get_yuan_from_fen(fen):
    """
    价格从分转换到元
    :param fen: int
    :return: double
    """
    #  yuan = Decimal.from_float(fen) / Decimal(100)
    #  return float(yuan.quantize(Decimal("1.00"), ROUND_HALF_UP))
    # 此处和其它模块保持一致，使用银行家四舍六入五成双算法
    return round(fen / 100., 2)


def get_fen_from_yuan(yuan):
    """
    价格从元转换到分
    :param yuan: double
    :return: int
    """
    # 对于整数 ivar, ivar 和 int((ivar / 100.) * 100)可能不等，如29, 57, 58等
    # 对于32位正整数来说，有：ivar == int((ivar / 100.) * 100 + 0.5)
    if yuan < 0:
        return -get_fen_from_yuan(-yuan)
    return int(yuan * 100 + 0.5)


def get_yuan_str_from_yuan_float(yuan, decimal_places=2, unit_prefix='¥'):
    """
    浮点数元精确指定小数点位数并返回字符串
    :param yuan: 1.00(float)
    :param decimal_places: 精确到小数点后几位
    :param unit_prefix: 字符串元前的前缀
    :return: str
    """
    # 采用四舍六入五成双算法精确小数点位数
    yuan_str = str(round(yuan, decimal_places))
    if '.' in yuan_str:
        yuan_str = yuan_str.rstrip('0').rstrip('.')
    return unit_prefix + yuan_str


def get_yuan_from_fen_abandon(fen, decimal_places=1):
    """
    价格从分转换到元，不进行四舍五入
    :param fen: int
    :param decimal_places: int
    :return: double
    """
    return truncate(fen / 100., decimal_places)


def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def get_yuan_str_from_fen(fen, decimal_places=2, unit_prefix=''):
    return get_yuan_str_from_yuan_float(get_yuan_from_fen(fen), decimal_places, unit_prefix)


def int_safe(value, default=0):
    """
    安全的类型转换器
    """
    try:
        return int(value)
    except:
        return default


def float_safe(value, default=0.0):
    try:
        return float(value)
    except:
        return default


def str_safe(value, default=''):
    try:
        return str(value)
    except:
        return default


def rand_num_str(length=8):
    return ''.join(random.choice(string.digits) for _ in range(length))
