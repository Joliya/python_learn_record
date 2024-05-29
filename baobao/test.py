"""
@file: test.py
@time: 2024/2/27 20:49
@desc: 
"""


import numpy as np

arr = np.array([-1, 0, 2, -3, 4])
result = np.any(arr > 0)
print(result)  # 输出：True

