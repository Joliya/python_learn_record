import sys


self_num = input().split("-")
used_num = input().split("-")
print(self_num, used_num)

m = {
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}

m_s = {
    11: "J",
    12: "Q",
    13: "K",
    14: "A"
}

self_num_map = {}
for j in self_num:
    i = m.get(j, j)
    index = int(i)
    num = self_num_map.get(index, 0)
    num += 1
    self_num_map[index] = num

used_num_map = {}
for j in used_num:
    i = m.get(j, j)
    index = int(i)
    num = used_num_map.get(index, 0)
    num_2 = self_num_map.get(index, 0)
    num = num + num_2 + 1
    used_num_map[index] = num

duishou = []
for i in range(3, 15):
    if used_num_map.get(i, 0) < 4:
        duishou.append(i)
print(duishou)
result = []
max_num = 0
for i in range(len(duishou)):
    r = []
    m_num = 0
    for j in range(i, len(duishou) + 1):
        if j == len(duishou) or (j > i and duishou[j] != duishou[j - 1] + 1):
            if m_num > max_num:
                result = r
                max_num = m_num
            elif m_num == max_num:
                result = r if r[-1] > result[-1] else result
            break
        else:
            r.append(duishou[j])
            m_num += 1
print("-".join([str(m_s.get(i, i)) for i in result]))


