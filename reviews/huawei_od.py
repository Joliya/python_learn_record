"""

"""

from __future__ import absolute_import, unicode_literals


def min_combined_students(people_count, question_count, student_data):
    student_data.sort()  # 将考生的正确题目范围按照起始位置排序
    combined_count = 0  # 初始化需要结合的考生数量
    current_max = 0  # 当前已经查看的题目的最大位置
    i = 0  # 考生数据的索引

    while i < people_count:
        if student_data[i][0] > current_max + 1:
            return -1  # 无法找到连续的考生覆盖所有题目

        max_end = current_max
        while i < people_count and student_data[i][0] <= current_max + 1:
            max_end = max(max_end, student_data[i][1])
            i += 1

        current_max = max_end
        combined_count += 1

        if current_max >= question_count:
            return combined_count

    return -1  # 无法找到连续的考生覆盖所有题目

# 读取输入
question_count = int(input())
people_count = int(input())
student_data = []
for _ in range(people_count):
    start, end = map(int, input().split())
    student_data.append((start, end))

result = min_combined_students(people_count, question_count, student_data)
print(result)


"""
10
4
1 3
1 7
4 6
6 10"""