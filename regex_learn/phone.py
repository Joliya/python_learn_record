# -*- encoding: utf-8 -*-
"""
手机号正则
"""

from __future__ import absolute_import, unicode_literals

import re


def is_phone(phone):
    """
    判断手机号是否正确
    :param phone:
    :return:
    """
    if re.match(r'^1[3-9]\d{9}$', phone):
        return True
    return False


if __name__ == '__main__':
    print(is_phone('13888888888'))
    print(is_phone('13011231231'))
