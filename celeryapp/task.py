# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals

import time

from celery import Celery

app = Celery('tasks', broker='amqp://guest@192.168.21.63:2181//')


@app.task
def x():
    print("任务开始")
    time.sleep(5)
    print("任务结束")
    return 1 + 2


if __name__ == '__main__':
    result = x.delay()
    print(result.ready())
    print(result.result)
    time.sleep(10)
    print(result.ready())
    print(result.result)
