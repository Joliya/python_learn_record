"""
@file: compute_word_time.py
@time: 2024/4/23 21:06
@desc: 
"""


time_list = [
    ("10:00", "21:20"),
    ("10:00", "21:39"),
    ("10:00", "21:02"),
    ("10:00", "21:18"),
    ("10:00", "21:09"),
    ("10:00", "21:01"),
    ("10:00", "20:45"),
    ("10:00", "20:40"),
    ("10:00", "21:05"),
    ("10:00", "21:10"),
    ("10:00", "21:26"),
    ("10:00", "21:10"),
    ("10:00", "21:13"),
    ("10:00", "21:29"),  # 22 号
    ("10:00", "21:15"),  # 23 号
    ("10:00", "21:17"),  # 24 号
    ("10:00", "21:03"),  # 27 号
    ("10:00", "20:20"),  # 28 号
]


def compute_time(t_list):
    """计算平均每天多少小时"""
    total_time = 0
    print(len(t_list))
    for start, end in t_list:
        start_hour, start_minute = map(int, start.split(":"))
        end_hour, end_minute = map(int, end.split(":"))
        total_time += end_hour - start_hour + (end_minute - 1 - start_minute) / 60
    return total_time / len(time_list)


if __name__ == '__main__':
    result = compute_time(time_list)
    print(f"平均时长：{round(result, 2)}")
    print(f"平均每天多余分钟数：{round((result - int(result)) * 60, 2)}")
