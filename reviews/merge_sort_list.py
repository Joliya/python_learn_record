
"""

"""

from __future__ import absolute_import, unicode_literals


def merge_sort_list(nums1, nums2):
    first, second = 0, 0
    nums1_len = len(nums1)
    nums2_len = len(nums2)
    new_nums = []
    while first < nums1_len and second < nums2_len:
        if nums1[first] <= nums2[second]:
            new_nums.append(nums1[first])
            first += 1
        else:
            new_nums.append(nums2[second])
            second += 1
    for i in range(first, nums1_len):
        new_nums.append(nums1[i])

    for j in range(second, nums2_len):
        new_nums.append(nums2[j])
    return new_nums


if __name__ == '__main__':
    nums1 = [2, 4, 7, 9]
    nums2 = [1, 3, 6, 9]
    print(merge_sort_list(nums1, nums2))

