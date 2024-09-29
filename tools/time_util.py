# coding:utf-8
'''
'''
import datetime
import time

FORMAT_DATETIME = u'%Y-%m-%d %H:%M:%S'
FORMAT_DATE_MINUTE = u'%Y-%m-%d %H:%M'
FORMAT_DATETIME_MSEC = u'%Y-%m-%d %H:%M:%S.%f'


def datetime_to_str(date, date_format=FORMAT_DATETIME, process_none=False):
    """
    convert {@see datetime} into date string ('2011-01-12')
    """
    if process_none and date is None:
        return ''
    return date.strftime(date_format)


def datetime_str_to_str(date_str, date_format=FORMAT_DATETIME, process_none=False):
    """
    convert date string ('2011-01-12') into date string ('2011-01-12')
    """
    date = str_to_datetime(date_str, FORMAT_DATETIME, process_none)
    return datetime_to_str(date, date_format, process_none)


def str_to_datetime(date_str, date_format=FORMAT_DATETIME, process_none=False):
    """
    convert date string ('2011-01-12') into {@see datetime}
    """
    if process_none and not date_str:
        return None
    date = datetime.datetime.strptime(date_str, date_format)
    return date


def gap_day(time_str, date=None, format="%Y-%m-%d"):
    """
    :判断自然日差几天
    :param time_str: 2019-02-19 21:49:20
    :return:
    """
    if not date:
        date = time.strftime(format)
    now_day_stamps = time.mktime(time.strptime(date, format))
    if " " in format:
        format = format.split(" ")[0]
    input_stamps = time.mktime(time.strptime(time_str.split(" ")[0], format))
    return int(abs((now_day_stamps - input_stamps)) // 86400)


def gap_stamps_day(time_str, now_day_stamps=None):
    """
    :判断绝对时间差几天
    :param time_str: 2019-02-19 21:49:20
    :return:
    """
    if not now_day_stamps:
        now_day_stamps = time.time()
    input_stamps = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
    return int(abs((now_day_stamps - input_stamps)) // 86400)


def gap_stamps_hour(time_str):
    """
    :判断绝对上差几个小时
    :param time_str: 2019-02-19 21:49:20
    :return:
    """
    now = int(time.time())
    input_stamps = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
    return int(abs((now - input_stamps)) // 3600)


def gap_stamps_minute(time_str):
    """
    :判断绝对上差几个分钟
    :param time_str: 2019-02-19 21:49:20
    :return:
    """
    now = int(time.time())
    input_stamps = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
    return int(abs((now - input_stamps)) // 60)


def get_time_stamp(timeStr, format="%Y-%m-%d %H:%M:%S"):
    """
        获取时间戳
    :param timeStr: 2019-05-12 09:00:00
    :param format: "%Y-%m-%d %H:%M:%S"
    :return:
    """
    time_array = time.strptime(timeStr, format)
    timestamp = time.mktime(time_array)
    return int(timestamp)


def gap_stamps_sec(time_str):
    """
    :判断绝对上差几秒
    :param time_str: 2019-02-19 21:49:20
    :return:
    """

    now = int(time.time())
    input_stamps = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
    return int(abs((now - input_stamps)))


def get_day_jia(date, n, format='%Y-%m-%d'):
    """
    时间加n天
    :param date:
    :param n:
    :return:
    """
    jia_date = datetime.datetime.strptime(date, format)
    jia_date = jia_date + datetime.timedelta(days=n)
    return jia_date.strftime(format)


def get_sec_jia(seconds, format="%Y-%m-%d %H:%M:%S"):
    """
    当前时间加多少秒
    :param seconds:
    :param format:
    :return: 2019-12-30 19:25:30
    """
    return (datetime.datetime.now() + datetime.timedelta(seconds=seconds)).strftime(format)


def get_ts_to_time(ts):
    """时间戳转字符串"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def day_long(time1, time2, format="%Y-%m-%d %H:%M:%S"):
    """
    计算时间差
    :return: 相差的天数
    """
    ts1 = get_time_stamp(time1, format)
    ts2 = get_time_stamp(time2, format)
    date1 = datetime.datetime.fromtimestamp(ts1)
    date2 = datetime.datetime.fromtimestamp(ts2)
    return abs(int((date2 - date1).days))


def get_sec_add(seconds, format="%Y-%m-%d %H:%M:%S"):
    """
    当前时间加多少秒
    :param seconds:
    :param format:
    :return: 2019-12-30 19:25:30
    """
    return (datetime.datetime.now() + datetime.timedelta(seconds=seconds)).strftime(format)


def time_diff(time_str):
    """
    :判断时间和服务器时间相差多少秒
    :param time_str: 2019-02-19 21:49:20
    :return:
    """

    now = int(time.time())
    input_stamps = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
    return int(input_stamps - now)


def days_ago_datetime_str(n):
    """
    获取n天前的日期的0时0分0秒
    :param n:
    :return:
    """
    today = datetime.date.today()
    days = datetime.timedelta(days=n)
    target_day = today - days
    return target_day.strftime("%Y-%m-%d 00:00:00")


def tomorrow_ts():
    """
    获取明天0点时间戳
    :return:
    """
    today = datetime.date.today()
    tomorrow = str(today + datetime.timedelta(days=1))
    return int(time.mktime(time.strptime(tomorrow, "%Y-%m-%d")))


def get_now_str(data_format="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间字符串
    :return:
    """
    return time.strftime(data_format)


if __name__ == "__main__":
    s = "231004198903150313"
    # print(int(gap_day(time_str="2019-11-22 11:04:58", format="%Y-%m-%d %H:%M:%S")))
    # print(time.strftime("%Y-%m-%d %H:%M:%S"))
    print(get_sec_jia(86400 * 2, format="%Y-%m-%d") + " 00:00:00")
    # print(get_time_stamp("2020-03-21 20:00:00"))
    # print(gap_stamps_sec("2020-05-12 17:33:49"))
