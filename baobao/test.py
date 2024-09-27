"""
@file: test.py
@time: 2024/2/27 20:49
@desc: 
"""

import pandas as pd


def find_combinations(data, target, start=0, path=[], result=None):
    if result is None:
        result = []
    # 如果目标小于0，或者起始位置超出范围，直接返回
    if target < 0 or start >= len(data):
        return
    # 如果目标正好为0，添加当前路径到结果
    if target == 0:
        result.append(path)
        print(result)
        return result
    for i in range(start, len(data)):
        # 选择当前元素，递归寻找剩余的
        find_combinations(data, target - data[i][1], i + 1, path + [data[i]], result)
    return result

# 示例数据

data = pd.read_excel("/workspace/python_learn_record/baobao/执行明细-6月.xlsx")
data.fillna("", inplace=True)
data = [(i[0], i[1]) for i in data.values]

# 目标数值
target = 1132400

# 查找组合
combinations = find_combinations(data, target)

# 打印结果
for combination in combinations:
    print(combination)
