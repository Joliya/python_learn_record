"""
@file: common.py
@time: 2023/11/22 15:03
@desc:
"""


def generate_page(page, page_size):
    start = (page - 1) * page_size
    end = start + page_size
    return start, end


def trim_non_number(version):
    """
    1. 删除version中的其他字符，例如: "Build 1.0" ==> "1.0"
    2. 如果version中不包含有效的数字，则返回"0"
    3. 假定: 如果version中存在数据，则所有的数字或者点一定时连续的，如: "Build 1.0.0", 不会出现: "Build 1.0.a.1"
    """
    if not version:
        return "0"
    start = None
    end = None
    idxs = list(range(len(version)))
    # 找第一个数字
    for i in idxs:
        if '0' <= version[i] <= '9':
            start = i
            break
    # 找后面第一个数字
    idxs.reverse()
    for i in idxs:
        if '0' <= version[i] <= '9':
            end = i + 1
            break
    return '0' if start is None else version[start: end]


def later_or_equal_version(v1, v2):
    """
    return weather v1 is a later or equal version than v2
    """
    try:
        # 防止出现空字符串
        v1 = trim_non_number(v1)
        v2 = trim_non_number(v2)

        info1 = v1.split('.')
        info2 = v2.split('.')
        for i, sub_version_tuple in enumerate(zip(info1, info2)):
            sub_v1, sub_v2 = sub_version_tuple
            # 诊所端有这样的版本号, 4.7.40630, 最后一段都是5位, 进行对齐操作
            if i == 2 and max(len(sub_v1), len(sub_v2)) == 5:
                sub_v1 += ('0' * (5 - len(sub_v1)))
                sub_v2 += ('0' * (5 - len(sub_v2)))
            if int(sub_v1) > int(sub_v2):
                return True
            elif int(sub_v1) < int(sub_v2):
                return False
        return len(info1) >= len(info2)
    except:
        return False


def compute_percent_by_base(numerator, denominator, can_direct=False, base_percent=10):
    """
    计算百分比
    :param can_direct: 直通
    :param numerator: 分子
    :param denominator: 分母
    :param base_percent: 基础百分比
    :return: 百分比
    """
    percent = compute_percent(numerator, denominator, can_direct)
    if percent <= 0:
        return 0
    return round(percent * 0.9 + base_percent, 2)


def compute_percent(numerator, denominator, can_direct=False):
    """
    计算百分比
    :param can_direct: 直通
    :param numerator: 分子
    :param denominator: 分母
    :return: 百分比
    """
    if can_direct:
        return 100
    if not denominator:
        return 0
    if numerator < 0:
        return 0
    percent = round(numerator / denominator * 100, 2)
    return min(percent, 100)


def compute_percent_int(numerator, denominator, can_direct=False):
    """
    计算百分比
    :param can_direct: 直通
    :param numerator: 分子
    :param denominator: 分母
    :return: 百分比
    """
    if can_direct:
        return 100
    if not denominator:
        return 0
    if numerator < 0:
        return 0
    percent = int(numerator / denominator * 100)
    return min(percent, 100)


def get_bit_val(byte, index):
    """
    :param byte: 待取值的字节值
    :param index: 待读取位的序号，从右向左0开始，0-7为一个完整字节的8个位
    :returns: 返回读取该位的值，0或1
    """
    if int(byte) & (1 << int(index)):
        return 1
    return 0


def get_bit_num(byte):
    if not byte:
        return 0
    return bin(int(byte))[2:].count("1")


def set_bit_val(byte, index, val):
    """
    更改某个字节中某一位（Bit）的值

    :param byte: 准备更改的字节原值
    :param index: 待更改位的序号，从右向左0开始，0-7为一个完整字节的8个位
    :param val: 目标位预更改的值，0或1
    :returns: 返回更改后字节的值
    """
    if val:
        return str(int(byte) | (1 << int(index)))
    if not get_bit_val(byte, index):
        return byte
    return str(int(byte) & ~(1 << int(index)))


def get_highest_bit_index(byte):
    # 将字符串转换为整数
    n = int(byte)
    if n == 0:
        return 0  # 如果byte为0，则没有位为1

    index = 0
    while n != 0:
        n >>= 1  # 将数字右移一位
        if n != 0:  # 如果右移后的数字不为0，则继续
            index += 1

    return index


def insert_list2_from_list1_at_index(list1, list2, index):
    """
    将list1 中的每一项插入到list2 的倒数index位置
    :param list1: 目标列表
    :param list2: 待插入列表
    :param index: 插入位置
    :return: None
    """
    if not list2 or not list1:
        return list2 or list1
    for item in list1:
        list2.insert(-index, item)
    return list2
