# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

import re


def find_image_url(html):
    """
    找到图片的url
    :param html:
    :return:
    """
    pattern = "http.*?jpg"
    r = re.findall(pattern=pattern, string=html)
    print(r)
    return r


if __name__ == '__main__':
    html_str = '<p><img src="https://resourced.chunyu.mobi/__8AAAAQ5MLX7-YW-14748d36-bf72-4da2-a8fd-da0c34d4b776_w800_h800_.jpg"><img src="https://resourced.chunyu.mobi/MgIAAACMPHvZ7-YW-10fb9a41-d300-49ac-bf08-7383738e1f82_w800_h800_.jpg"><img src="https://resourced.chunyu.mobi/eKUAAADtUhzb7-YW-b709ab71-fcdb-485a-ab90-2c39e3375257_w800_h800_.jpg"><img src="https://resourced.chunyu.mobi/elsAAACUBZPc7-YW-b8c9a008-5099-4e59-9f4e-90ddf5bc0bea_w800_h800_.jpg"></p>'
    for i in find_image_url(html_str):
        print(i)
