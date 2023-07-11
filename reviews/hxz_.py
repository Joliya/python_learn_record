"""
1、乘客打车时间段是上午是8:10到9:10，
下午是17:10到19:20。司机可以接单时间是9:00到12:00，下午是14:00到18:00。司机和乘客可能撮合匹配交集时间9:00到9:10和17:10到18:00
 1 2 3
 1 2 3
 1 2 3


2、有一个 n 个格子 的网格，规则是黑白双方交替落子，每次只能落1个，当落满棋盘的时候最后一个落子的一方胜利，求n什么情况下先落子胜


如果每次可以下 1-3 个，
其实就是必胜策略， n 为4 的倍数， 先下的人一定下不到4，后下的人总是保持 刚好下4的倍数就行，
n 不是 4 的倍数的情况下， 先下的人只要保证 留下的数量 是4的倍数， 后续的操作就是和 上面一样， 先下的人总是刚好下到4的倍数的格子

当 n 是 4 的倍数时，后下的人（B）存在必胜策略。
当 n 不是 4 的倍数时，先下的人（A）存在必胜策略。


"""
# custom_time_list = [(8:10, 9:10), (17:10, 19:20)]
# driver_time_list = [(9: 00, 12:10), (14:00, 18:00)]

# 输出 匹配交集


def find_intersection_times(passenger_times, driver_times):
    intersection_times = []

    for passenger_time in passenger_times:
        for driver_time in driver_times:
            start_time = max(passenger_time[0], driver_time[0])
            end_time = min(passenger_time[1], driver_time[1])

            if start_time < end_time:
                intersection_times.append((start_time, end_time))

    return intersection_times


def find_intersection_times_sort_list(passenger_times, driver_times):
    intersection_times = []

    i = 0  # 乘客时间段指针
    j = 0  # 司机时间段指针

    while i < len(passenger_times) and j < len(driver_times):
        passenger_start, passenger_end = passenger_times[i]
        driver_start, driver_end = driver_times[j]

        # 计算交集开始时间和结束时间
        start_time = max(passenger_start, driver_start)
        end_time = min(passenger_end, driver_end)

        if start_time < end_time:
            intersection_times.append((start_time, end_time))

        # 移动指针
        if passenger_end < driver_end:
            i += 1
        else:
            j += 1

    return intersection_times


if __name__ == '__main__':
    passenger_times = [(8.10, 9.10), (17.10, 19.20)]
    driver_times = [(9.00, 12.00), (14.00, 18.00)]

    intersection_times = find_intersection_times(passenger_times, driver_times)

    print(intersection_times)

    print(find_intersection_times_sort_list(passenger_times, driver_times))
